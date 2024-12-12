"""环境准备"""
import os
import tempfile
from lbkit import errors
from lbkit.tools import Tools


src_cwd = os.path.split(os.path.realpath(__file__))[0]

class MakeImage():
    def __init__(self, tmp_dir):
        self.tools = Tools("make emmc_image")
        self.log = self.tools.log
        self.size_1m = 4096
        self.misc_blk_1k = 1024
        self.ubootenv_blk_1k = 1024
        self.vbmeta_blk_1k = 1024
        # 会创建3个rootfs镜像
        self.rootfs_blk_1m = 1024
        # 用户数据区最小512m
        self.userdata_blk_1m = 512
        self.tmp_dir = tmp_dir
        if not os.path.isdir(tmp_dir):
            os.makedirs(self.tmp_dir)
        else:
            cmd = "umount " + tmp_dir
            self.tools.exec(cmd, ignore_error=True, echo_cmd=False)

    def run(self, dtb, rootfs, output="emmc.img"):
        blk_1k = self.misc_blk_1k + self.ubootenv_blk_1k + self.vbmeta_blk_1k
        blk_1k += self.rootfs_blk_1m * 1024 * 3
        blk_1k += self.userdata_blk_1m * 1024
        if self.size_1m * 1024 < blk_1k:
            blk_1m = int((blk_1k + 1023) / 1024)
            raise errors.LiteBmcException(f"参数检测错误，镜像文件{self.size_1m}M小于需要的{blk_1m}M大小")
        if self.userdata_blk_1m == 512:
            self.userdata_blk_1m = int(self.size_1m - blk_1k / 1024) - 128
            self.log.info(f"重置userdata大小为{self.userdata_blk_1m}M")
        if os.path.isfile(output):
            os.unlink(output)
        self.log.info(f"创建一个{self.size_1m}M大小的镜像")
        self.tools.exec(f"dd if=/dev/zero of={output} bs=1M count=1 seek={self.size_1m -1}")
        self.tools.exec(f"parted {output} mktable gpt")
        start = 4096
        end = start + self.misc_blk_1k * 2
        self.log.info(f"创建misc区")
        self.tools.exec(f"parted {output} mkpart misc {start}s {end - 1}s")
        start = end
        end += self.ubootenv_blk_1k * 2
        self.log.info(f"创建ubootenv区")
        self.tools.exec(f"parted -s -a none {output} mkpart ubootenv {start}s {end - 1}s")
        start = end
        end += self.vbmeta_blk_1k * 2
        self.log.info(f"创建vbmeta区")
        self.tools.exec(f"parted -s -a none {output} mkpart vbmeta {start}s {end - 1}s")
        start = end
        end += self.rootfs_blk_1m * 1024 * 2
        self.log.info("创建rootfs镜像区")
        self.tools.exec(f"parted -s -a none {output} mkpart rootfs_a {start}s {end - 1}s")
        self.log.info(f"挂载rootfs分区并复制内容，注意，此时会修改原始{rootfs}镜像并添加dtb以及启动参数")
        self.tools.exec(f"fuse2fs {rootfs} {self.tmp_dir} -o fakeroot -o nonempty")
        extlinux = os.path.join(self.tmp_dir, "boot/extlinux")
        os.makedirs(extlinux, exist_ok=True)
        with open(os.path.join(extlinux, "extlinux.conf"), "w+") as fp:
            fp.write("menu title U-Boot menu\n")
            fp.write("prompt 0\n")
            fp.write("timeout 10\n")
            fp.write("\n")
            fp.write("label litebmc-active\n")
            fp.write("    kernel /boot/Image\n")
            fp.write("    fdt /boot/litebmc.dtb\n")
            fp.write("    append console=ttyAMA0 loglevel=10 rootwait root=/dev/nvme0n1p4 rw\n")
        self.tools.exec(f"cp {dtb} {self.tmp_dir}/boot/litebmc.dtb")
        self.tools.exec(f"chown 0:0 {self.tmp_dir}/boot/ -R")
        self.tools.exec(f"chmod 700 {self.tmp_dir}/boot/extlinux/")
        self.tools.exec(f"chmod 600 {self.tmp_dir}/boot/extlinux/extlinux.conf")
        self.tools.exec(f"chmod 600 {self.tmp_dir}/boot/Image")
        self.tools.exec(f"chmod 600 {self.tmp_dir}/boot/litebmc.dtb")
        self.tools.exec(f"umount {self.tmp_dir}")
        self.log.info("复制镜像文件到rootfs_a区域")
        self.tools.exec(f"dd if={rootfs} of={output} bs=512 seek={start} conv=notrunc")
        self.log.info("制作rootfs_b")
        start = end
        end += self.rootfs_blk_1m * 1024 * 2
        self.tools.exec(f"parted -s -a none {output} mkpart rootfs_b {start}s {end - 1}s")
        self.log.info("复制镜像文件到rootfs_b")
        self.tools.exec(f"dd if={rootfs} of={output} bs=512 seek={start} conv=notrunc")
        self.log.info("制作rootfs_c")
        start = end
        end += self.rootfs_blk_1m * 1024 * 2
        self.tools.exec(f"parted -s -a none {output} mkpart rootfs_c {start}s {end - 1}s")
        self.log.info("复制镜像文件到rootfs_c")
        self.tools.exec(f"dd if={rootfs} of={output} bs=512 seek={start} conv=notrunc")
        start = end
        self.log.info("制作userdata区")
        end += self.userdata_blk_1m * 1024 * 2
        self.tools.exec(f"parted -s -a none {output} mkpart userdata ext4 {start}s {end - 1}s")
        self.log.info("为userdata区创建一个空镜像")
        tmpfile = tempfile.NamedTemporaryFile()
        empty_img = tmpfile.name
        self.tools.exec(f"dd if=/dev/zero of={empty_img} bs=1M seek={self.userdata_blk_1m - 1} count=1")
        self.tools.exec(f"mkfs.ext4 {empty_img}")
        self.log.info("复制空镜像到userdata区")
        self.tools.exec(f"dd if={empty_img} of={output} bs=512 seek={start} conv=notrunc")
        self.tools.exec(f"parted {output} set 4 boot on")

if __name__ == "__main__":
    mk = MakeImage()
    mk.run("./Image", "./virt.dtb", "./rootfs.img", "./qemu.img")

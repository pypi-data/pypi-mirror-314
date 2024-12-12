"""环境准备"""
import os
import tarfile
from lbkit.integration.config import Config
from lbkit.integration.task import Task
from lbkit.log import Logger
from lbkit import errors
from lbkit.utils.images.emmc import MakeImage as MekeEmmcImage

log = Logger("build_image")

src_cwd = os.path.split(os.path.realpath(__file__))[0]

class BuildImage(Task):
    @staticmethod
    def _trans_to_blk_1m(cfg: str):
        if cfg.endswith("K"):
            return int(cfg[:-1]) / 1024
        elif cfg.endswith("M"):
            return int(cfg[:-1])
        elif cfg.endswith("G"):
            return int(cfg[:-1]) * 1024

    def run(self):
        """任务入口"""
        """检查manifest文件是否满足schema格式描述"""
        os.chdir(self.config.output_path)
        cmd = "qemu-system-aarch64 -M virt -cpu cortex-a57 -M virt,dumpdtb=virt.dtb"
        self.exec(cmd)

        mk = MekeEmmcImage(os.path.join(self.config.temp_path, "emmc_tmp_dir"))
        rootfs_size = self.get_manifest_config("metadata/rootfs_size")
        if rootfs_size:
            mk.rootfs_blk_1m = self._trans_to_blk_1m(rootfs_size)
        emmc_size = self.get_manifest_config("metadata/emmc_size")
        if emmc_size:
            mk.size_1m = self._trans_to_blk_1m(emmc_size)
        mk.run("virt.dtb", self.config.rootfs_img, "qemu.img")
        cmd = 'cp /usr/share/litebmc/qemu.conf qemu.conf'
        self.exec(cmd)
        output_img = os.path.join(self.config.output_path, "litebmc_qemu.tar.gz")
        cmd = f'tar -czf {output_img} -C . qemu.img {self.config.uboot_bin} qemu.conf'
        self.exec(cmd)
        log.success(f"Create litebmc image {output_img} successfully")

if __name__ == "__main__":
    config = Config()
    build = BuildImage(config)
    build.run()
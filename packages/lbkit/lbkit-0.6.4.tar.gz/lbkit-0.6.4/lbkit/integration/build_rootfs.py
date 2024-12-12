"""完成rootfs镜像打包."""
import os
import shutil
import tarfile
from lbkit.integration.config import Config
from lbkit.integration.task import Task
from lbkit.log import Logger
from lbkit import errors

log = Logger("build_rootfs")

src_cwd = os.path.split(os.path.realpath(__file__))[0]
IMG_FILE = "rootfs.img"

class BuildRootfs(Task):
    """构建rootfs镜像"""
    def do_permission(self, per_file: str):
        """完成组件制品赋权"""
        if not os.path.isfile(per_file):
            return
        log.info("Do permission, file: %s", per_file)
        with open(per_file, "r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if line.startswith("#") or len(line) == 0:
                    continue
                log.debug("Permission line: %s", line)
                chunk = line.split()
                if len(chunk) < 5:
                    raise errors.PermissionFormatError(f"Permission format with error, line: {line}")
                if not chunk[0].startswith("/"):
                    raise errors.PermissionFormatError(f"Permission file error, must begin with \"/\", get: {chunk[0]}")
                if not chunk[3].isnumeric() or not chunk[4].isnumeric():
                    raise errors.PermissionFormatError(f"Permission uid or gid error, must is numeric, uid({chunk[3]}), gid({chunk[4]})")
                chunk[0] = chunk[0].lstrip("/")
                if chunk[1] != "f" and chunk[1] != "d" and chunk[1] != "s" and chunk[1] != "r":
                    raise errors.PermissionFormatError(f"Permission type error, only support 'f' 's' 'd' 'r', get({chunk[1]}), ignore")
                if chunk[1] == "d" and not os.path.isdir(chunk[0]):
                    log.error("Permission error, %s is not directory", chunk[0])
                if chunk[1] == "s" and not os.path.islink(chunk[0]):
                    log.error("Permission error, %s is not directory", chunk[0])
                uid = int(chunk[3])
                gid = int(chunk[4])
                pri = chunk[2]
                if (chunk[1] == "f" and os.path.isdir(chunk[0])) or chunk[1] == "r":
                    for subf in os.listdir(chunk[0]):
                        file_path = os.path.join(chunk[0], subf)
                        if not os.path.isfile(file_path):
                            continue
                        log.debug("chmod %s", file_path)
                        cmd = f"chmod {pri} {file_path}"
                        self.exec(cmd)
                        cmd = f"chown {uid}:{gid} {file_path}"
                        self.exec(cmd)
                else:
                    cmd = f"chmod {pri} {chunk[0]}"
                    self.exec(cmd)
                    cmd = f"chown {uid}:{gid} {chunk[0]}"
                    self.exec(cmd)

    def copy_conan_install(self, src_dir, mnt_path):
        src_dir += "/"
        cmd = f"rsync -aHK --exclude '*.hpp' --exclude '*.h'"
        cmd += f" --exclude 'rootfs.tar' --exclude 'u-boot.bin'"
        cmd += f" --exclude 'conanmanifest.txt' --exclude 'conaninfo.txt'"
        cmd += f" --exclude '*.a' --chown=0:0 {src_dir} {mnt_path}"
        log.info("copy %s to %s", src_dir, mnt_path)
        self.exec(cmd, echo_cmd=False)
        strip = self.get_manifest_config("metadata/strip")
        for root, dirs, files in os.walk(src_dir):
            root = root.replace(src_dir, "")
            for dir in dirs:
                name = os.path.join(mnt_path, root, dir)
                if not os.path.isdir(name):
                    continue
                cmd = f"chown 0:0 {name}"
                self.exec(cmd, echo_cmd=False)
            for file in files:
                name = os.path.join(mnt_path, root, file)
                cmd = f"chown -h 0:0 {name}"
                if not os.path.isfile(name):
                    continue
                self.exec(cmd, echo_cmd=False)
                if name.find("usr/share") > 0 and name.find("bin") == -1:
                    continue
                suffix = name.split(".")[-1]
                no_need_strip = ["json", "html", "md", "txt", "yaml", "xml"]
                no_need_strip.extend(["yml", "mo", "conf", "gz", "inc", "service", "py"])
                no_need_strip.extend(["m4", "pc", "cmake", "rules", "ts", "js", "png"])
                no_need_strip.extend(["jpg", "jpeg", "mpeg", "c", "h", "hpp"])
                if suffix != name and suffix in no_need_strip:
                    continue
                strip = self.get_manifest_config("metadata/strip")
                if strip:
                    cmds = [f"file {name}", "grep \"not stripped\"", f"{self.config.strip} -s {name}"]
                    self.pipe(cmds, error_log="", ignore_error=True)
        per_file = os.path.join(src_dir, "permissions")
        self.do_permission(per_file)

    def merge_rootfs(self):
        """将产品依赖的所有组件安装到rootfs镜像中"""
        mnt_path = self.config.mnt_path
        self.exec("umount " + mnt_path, ignore_error=True)
        shutil.rmtree(mnt_path, ignore_errors=True)
        os.makedirs(mnt_path)
        # 按manifest配置的大小调整rootfs
        rootfs_size = self.get_manifest_config("metadata/rootfs_size")
        if self.config.rootfs_tar:
            cmd = f"mkfs.ext4 -d {mnt_path} -r 1 -N 0 -m 5 -L \"rootfs\" -O ^64bit {self.config.rootfs_img} \"{rootfs_size}\""
            self.exec(cmd)
        # 挂载rootfs镜像
        self.exec(f"fuse2fs {self.config.rootfs_img} {mnt_path} -o fakeroot")
        # 从rootfs.tar解压内容
        if self.config.rootfs_tar:
            cmd = f"tar -pxf {self.config.rootfs_tar} -C {mnt_path} ."
            self.exec(cmd)
            cmd = f"chown root:root {mnt_path} -R"
            self.exec(cmd)
        # 切换到rootfs挂载目录
        os.chdir(mnt_path)
        log.info("Copy customization rootfs......")
        for src_dir in self.config.conan_install:
            self.copy_conan_install(src_dir, mnt_path)

        # copy product self-owned rootfs
        product_rootfs = os.path.join(self.config.work_dir, "rootfs")
        if os.path.isdir(product_rootfs):
            self.copy_conan_install(product_rootfs, mnt_path)

        # 执行rootfs定制化脚本
        os.chdir(self.config.work_dir)
        hook_name = "hook.post_rootfs"
        self.do_hook(hook_name)

        # 清理冗余文件
        inc_dir = os.path.join(self.config.mnt_path, "include")
        if os.path.isdir(inc_dir):
            cmd = "rm -rf " + inc_dir
            self.exec(cmd)
        cmd = "rm " + os.path.join(self.config.mnt_path, "permissions")
        self.exec(cmd)

        log.info("remove all .fuse_hiddeng* files")
        cmds = [f"find {self.config.mnt_path} -name .fuse_hidden*", "xargs -i{} rm {}"]
        self.pipe(cmds)
        self.exec("umount " + mnt_path)

    def run(self):
        # 任务入口
        self.merge_rootfs()
        log.success(f"Create image {self.config.rootfs_img} successfully")

if __name__ == "__main__":
    config = Config()
    build = BuildRootfs(config)
    build.run()
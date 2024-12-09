"""应用构建任务"""
import os
import shutil
import json
from mako.lookup import TemplateLookup
from lbkit.integration.config import Config
from lbkit.integration.task import Task
from lbkit.log import Logger
from lbkit.build_conan_parallel import BuildConanParallel
from concurrent.futures import ThreadPoolExecutor
from lbkit.errors import LiteBmcException

log = Logger("product_build")


class ManifestValidateError(OSError):
    """Raised when validation manifest.yml failed."""

src_cwd = os.path.split(os.path.realpath(__file__))[0]

class BuildManifest(Task):
    """根据产品配置构建所有app,记录待安装应用路径到self.config.conan_install路径"""
    def __init__(self, cfg: Config, name: str):
        super().__init__(cfg, name)
        self.conan_build = os.path.join(self.config.temp_path, "conan")
        if os.path.isdir(self.conan_build):
            shutil.rmtree(self.conan_build)
        os.makedirs(self.conan_build)
        if self.config.build_type == "debug":
            self.conan_settings = " -s build_type=Debug"
        elif self.config.build_type == "release":
            self.conan_settings = " -s build_type=Release"
        elif self.config.build_type == "minsize":
            self.conan_settings = " -s build_type=MinSizeRel"
        self.common_args = "-r " + self.config.remote
        self.common_args += " -pr:b {} -pr:h {}".format(self.config.profile_build, self.config.profile_host)
        self.common_args += " -o */*:test=False"

    def deploy(self, graph_file):
        with open(graph_file, "r") as fp:
            graph = json.load(fp)
        nodes = graph.get("graph", {}).get("nodes", {})
        for id, info in nodes.items():
            ref = info.get("ref")
            id = info.get("package_id")
            context = info.get("context")
            if context != "host" or ref.startswith("litebmc/"):
                continue
            cmd = f"conan cache path {ref}:{id}"
            package_folder = self.tools.run(cmd).stdout.strip()
            rootfs_tar = os.path.join(package_folder, "rootfs.tar")
            uboot_bin = os.path.join(package_folder, "u-boot.bin")
            linux_bin = os.path.join(package_folder, "boot/Image")
            if os.path.isfile(rootfs_tar):
                self.config.rootfs_tar = rootfs_tar
                continue
            elif os.path.isfile(uboot_bin):
                self.config.uboot_bin = uboot_bin
                continue
            elif os.path.isfile(linux_bin):
                self.config.linux_bin = linux_bin
            self.config.conan_install.append(package_folder)

    def download_recipe(self, pkg):
        cmd = f"conan cache path {pkg}"
        ret = self.exec_easy(cmd, ignore_error=True)
        if ret is None or ret.returncode != 0:
            cmd = f"conan download {pkg} -r {self.config.remote} --only-recipe"
            self.exec(cmd, ignore_error=True)

    def build_litebmc(self):
        """构建产品conan包"""
        log.info("build litebmc")

        manifest = self.load_manifest()
        hook_name = "hook.prepare_manifest"
        self.do_hook(hook_name)
        # 使用模板生成litebmc组件的配置
        lookup = TemplateLookup(directories=os.path.join(src_cwd, "template"))
        template = lookup.get_template("conanfile.py.mako")
        conanfile = template.render(lookup=lookup, pkg=manifest)

        recipe = os.path.join(self.conan_build, "litebmc")
        os.makedirs(recipe, exist_ok=True)
        os.chdir(recipe)
        fp = open("conanfile.py", "w", encoding="utf-8")
        fp.write(conanfile)
        fp.close()

        base_cmd = f"{self.common_args} {self.conan_settings}"
        lockfile = os.path.join(self.config.code_path, "conan.lock")
        threadPool = ThreadPoolExecutor(max_workers=16)
        # 指定-l参数或conan.lock文件不存在时创建lock文件
        if self.config.create_conan_lock or not os.path.isfile(lockfile):
            # 创建新的conan.lock文件
            for dep in manifest.get("dependencies", []):
                pkg = dep.get("package")
                threadPool.submit(self.download_recipe, pkg)
            lock_cmd = f"conan lock create . {base_cmd} --lockfile-out={lockfile}"
            self.exec(lock_cmd)
        else:
            with open(lockfile, "r") as fp:
                lock = json.load(fp)
            for key in ["requires", "build_requires", "python_requires", "config_requires"]:
                requires = lock.get(key, [])
                for require in requires:
                    threadPool.submit(self.download_recipe, require)
        threadPool.shutdown(wait=True)
        graph_cmd = f"conan graph info . {base_cmd} -f json --lockfile={lockfile}"
        graphfile = os.path.join(self.config.temp_path, "graph.info")
        self.pipe([graph_cmd], out_file=graphfile)
        bcp = BuildConanParallel(graphfile, lockfile, self.common_args, self.config.from_source)
        bcp.build()

        # 部署应用到self.config.conan_install
        self.deploy(graphfile)

    def run(self):
        """任务入口"""
        self.build_litebmc()
        error = False
        if not self.config.rootfs_tar:
            error = True
            self.log.error("rootfs.tar not found in any conan package")
        if not self.config.uboot_bin:
            error = True
            self.log.error("u-boot.bin not found in any conan package")
        if not self.config.linux_bin:
            error = True
            self.log.error("boot/Image not found in any conan package")
        if error:
            raise FileNotFoundError("Build failed because important files are missing")

if __name__ == "__main__":
    config = Config()
    build = BuildManifest(config)
    build.run()

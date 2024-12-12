"""环境准备"""
import os
import shutil
import jinja2
import configparser
from lbkit.integration.config import Config
from lbkit.integration.task import Task
from lbkit.log import Logger

log = Logger("product_prepare")


class ManifestValidateError(OSError):
    """Raised when validation manifest.yml failed."""

src_cwd = os.path.split(os.path.realpath(__file__))[0]

class BuildPrepare(Task):
    def load_conan_profile(self):
        profile = self.get_manifest_config("metadata/profile")
        if not os.path.isfile(profile):
            raise FileNotFoundError(f"profile {profile} not found")
        log.info("Copy profile %s", profile)
        profiles_dir = os.path.expanduser("~/.conan2/profiles")
        if not os.path.isdir(profiles_dir):
            cmd = "conan profile detect -f"
            self.exec(cmd, ignore_error=True)
        dst_profile = os.path.join(profiles_dir, os.path.basename(profile))
        if os.path.isdir(profiles_dir):
            shutil.copyfile(profile, dst_profile, follow_symlinks=False)

        with open(dst_profile, "r") as fp:
            profile_data = jinja2.Template(fp.read()).render()
            parser = configparser.ConfigParser()
            parser.read_string(profile_data)
            strip = "strip"
            if parser.has_option("buildenv", "STRIP"):
                strip = parser.get("buildenv", "STRIP")
            path = ""
            if parser.has_option("buildenv", "PATH+"):
                path = parser.get("buildenv", "PATH+")
                if path.startswith("(path)"):
                    path = path[6:]
            elif parser.has_option("buildenv", "PATH"):
                path = parser.get("buildenv", "PATH")
                if path.startswith("(path)"):
                    path = path[6:]
            self.config.strip = os.path.join(path, strip)

    def run(self):
        """任务入口"""
        """检查manifest文件是否满足schema格式描述"""
        self.config.load_manifest()
        self.load_conan_profile()

if __name__ == "__main__":
    config = Config()
    build = BuildPrepare(config)
    build.run()
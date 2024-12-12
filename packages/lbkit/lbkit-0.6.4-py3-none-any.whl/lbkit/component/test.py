"""组件测试"""
import shutil
import re
import os
import importlib.machinery
import unittest
from lbkit.component.build import BuildComponent
from lbkit.component.arg_parser import ArgParser
from lbkit import errors
from lbkit.tools import Tools
from lbkit.misc import Color

tool = Tools("comp_test")
log = tool.log
cwd = os.getcwd()


class TestComponent():
    def __init__(self, args=None):
        self.build_parser = ArgParser.new(True)
        self.build_parser.parse_args(args) # 共享命令参数
        self.origin_args = args
        self.origin_args.append("--cov")
        self.origin_args.append("--test")
        self.package_id = ""

    def _collect_coverage_data(self, build_folder, test_src_folder):
        coverage_dir = os.path.join(".temp/coverage")
        shutil.rmtree(coverage_dir, ignore_errors=True)
        os.makedirs(coverage_dir)
        # 覆盖率数据路径由conanbase.make在build配置cflags时定义
        cmd = f"lcov -c -q -d {build_folder} -o {coverage_dir}/cover.info"
        tool.exec(cmd)
        for dir in test_src_folder:
            cmd = f"lcov -r  {coverage_dir}/cover.info \"{build_folder}/{dir}/*\" -o {coverage_dir}/cover.info"
            tool.exec(cmd)
        cmd = f"lcov -r  {coverage_dir}/cover.info \"*/include/*\" -o {coverage_dir}/cover.info"
        tool.exec(cmd)
        cmd = f"genhtml -o {coverage_dir}/html --legend {coverage_dir}/cover.info"
        tool.exec(cmd)

        index_file = os.path.join(coverage_dir, "html/index.html")
        with open(index_file, "r") as fp:
            content = fp.read()
        matches = re.search(r"Lines:</td\>\n.*headerCovTableEntry\"\>([0-9]+).*\n.*headerCovTableEntry\"\>([0-9]+).*\n.*headerCovTableEntry(Lo|Hi|Med)\"\>([0-9.]+) %", content)
        if matches is None:
            raise errors.LiteBmcException(f"Read line coverage data from {index_file} failed")
        line_hit = int(matches.group(1))
        line_total = int(matches.group(2))
        line_cov = float(matches.group(4))
        line_level = matches.group(3)
        log.info("Coverage info:")
        if line_level == "Hi":
            log.info(Color.GREEN + f"Line:     hit %-10d total %-10d coverage %.02f %% (High)" % (line_hit, line_total, line_cov) + Color.RESET_ALL)
        elif line_level == "Med":
            log.info(Color.YELLOW + f"Line:     hit %-10d total %-10d coverage %.02f %% (Medium)" % (line_hit, line_total, line_cov) + Color.RESET_ALL)
        elif line_level == "Lo":
            log.info(Color.RED + f"Line:     hit %-10d total %-10d coverage %.02f %% (Low)" % (line_hit, line_total, line_cov) + Color.RESET_ALL)
        matches = re.search(r"Functions:</td\>\n.*headerCovTableEntry\"\>([0-9]+).*\n.*headerCovTableEntry\"\>([0-9]+).*\n.*headerCovTableEntry(Lo|Hi|Med)\"\>([0-9.]+) %", content)
        if matches is None:
            raise errors.LiteBmcException(f"Read function coverage data from {index_file} failed")
        func_hit = int(matches.group(1))
        func_total = int(matches.group(2))
        func_cov = float(matches.group(4))
        func_level = matches.group(3)
        if func_level == "Hi":
            log.info(Color.GREEN + f"Function: hit %-10d total %-10d coverage %.02f %% (High)" % (func_hit, func_total, func_cov) + Color.RESET_ALL)
        elif func_level == "Med":
            log.info(Color.YELLOW + f"Function: hit %-10d total %-10d coverage %.02f %% (Medium)" % (func_hit, func_total, func_cov) + Color.RESET_ALL)
        elif func_level == "Lo":
            log.info(Color.RED + f"Function: hit %-10d total %-10d coverage %.02f %% (Low)" % (func_hit, func_total, func_cov) + Color.RESET_ALL)

    def _make_ld_library_path(self, rootfs_dir):
        cmd = f"find {rootfs_dir} -name *.so"
        res = tool.run(cmd)
        files = res.stdout.strip().split("\n")
        ld_library_path = os.environ.get("LD_LIBRARY_PATH", "").strip()
        library_path = []
        if ld_library_path != "":
            library_path = ld_library_path.split(":")
        for file in files:
            dir = os.path.dirname(file)
            if dir not in library_path:
                library_path.append(dir)
        os.environ["LD_LIBRARY_PATH"] = ":".join(library_path)

    def run(self):
        # 构建组件
        build = BuildComponent(self.build_parser, self.origin_args)
        build.run()

        self._make_ld_library_path(build.rootfs_dir)

        # 为确保路径正确，切换到初始路径
        os.chdir(cwd)
        # 必须存在test.py时才测试
        if not os.path.isfile("test.py"):
            log.warn("Test file(test.py) not exist, skip test")
            return 0
        # 从test.py加载LiteBmcComponentTest实例并运行用命
        loader = importlib.machinery.SourceFileLoader("test", os.path.join(cwd, "test.py"))
        mod = loader.load_module()
        klass = getattr(mod, "LiteBmcComponentTest")
        if klass is None:
            log.warn("test.py does not provide the LiteBmcComponentTest class, skip test")
            return 0
        test = klass(rootfs_dir=build.rootfs_dir)
        test_method = getattr(test, "test")
        if test_method is None:
            log.warn("The LiteBmcComponentTest class provided by test.py does not provide test methods, skip test")
            return 0

        log.success("call test method...")
        ret = test.test()
        if ret is not None:
            if isinstance(ret, unittest.TestResult) and (len(ret.errors) > 0 or len(ret.failures) > 0):
                raise errors.TestException(f"Test failed, ret: {ret}")
            elif isinstance(ret, int) and ret != 0:
                raise errors.TestException(f"Test failed, ret: {ret}")

        test_src_folder = getattr(test, "test_src_folder", [])
        # 设置ROOTFS_DIR环境变量，为DT测试提供相对路径
        self._collect_coverage_data(build.build_folder, test_src_folder)
        log.success("Test finished")


# GCOV_PREFIX和GCOV_PREFIX_STRIP用于指定不同目录或层级生成gcda文件
# 参考网址: https://gcc.gnu.org/onlinedocs/gcc/Cross-profiling.html
"""
    DBus接口代码自动生成
"""
import os
import sys
import json
import yaml
import argparse
from lbkit.codegen.idf_interface import IdfInterface

from mako.lookup import TemplateLookup
from lbkit.log import Logger
from lbkit.helper import Helper
from lbkit.errors import ArgException
from lbkit.misc import SmartFormatter

lb_cwd = os.path.split(os.path.realpath(__file__))[0]
log = Logger("codegen")

__version__=3

class CodeGen(object):
    def __init__(self, args):
        self.args = args
        self.codegen_version = __version__
        pass

    def _gen(self, idf_file, directory="."):
        directory = os.path.realpath(directory)
        os.makedirs(os.path.join(directory, "public"), exist_ok=True)
        os.makedirs(os.path.join(directory, "server"), exist_ok=True)
        os.makedirs(os.path.join(directory, "client"), exist_ok=True)
        interface = self.get_interface(idf_file)
        out_file = os.path.join(directory, "public", interface.name + ".xml")
        interface.render_dbus_xml("interface.introspect.xml.mako", out_file, self.codegen_version)
        for code_type in ["server", "client", "public"]:
            out_file = os.path.join(directory, code_type, interface.name + ".h")
            interface.render_c_source(code_type + ".h.mako", out_file, self.codegen_version)
            out_file = os.path.join(directory, code_type, interface.name + ".c")
            interface.render_c_source(code_type + ".c.mako", out_file, self.codegen_version)
        json_file = os.path.join(directory, "package.yml")
        data = {
            "version": interface.version,
            "name": interface.name
        }
        with open(json_file, "w", encoding="utf-8") as fp:
            yaml.dump(data, fp, encoding='utf-8', allow_unicode=True)

        # 生成接口schema文件
        odf_file = os.path.join(directory, "server", "schema", f"{interface.name}.json")
        os.makedirs(os.path.dirname(odf_file), exist_ok=True)
        odf_data = interface.odf_schema
        with open(odf_file, "w", encoding="utf-8") as fp:
            json.dump(odf_data, fp, sort_keys=False, indent=4)

    def get_interface(self, idf_file):
        lookup = TemplateLookup(directories=os.path.join(lb_cwd, "template"))
        return IdfInterface(lookup, idf_file)

    def run(self):
        """
        代码自动生成.

        支持自动生成服务端和客户端C代码
        """
        parser = argparse.ArgumentParser(description=self.run.__doc__,
                                         prog="lbkit gen",
                                         formatter_class=SmartFormatter)
        # 默认的自动生成工具版本号为2
        parser.add_argument("-cv", "--codegen_version", help=f'''must less than or equal to {__version__}, default: 2
                            description of changes:
                            3: compatible with lb_base/0.7.x
                            2: compatible with lb_base/0.6.x
                            ''',
                            type=int, default=2)
        parser.add_argument("-d", "--directory", help='generate code directory', default=".")
        group2 = parser.add_argument_group('cdf file', 'Generate code using the specified CDF file')
        group2.add_argument("-c", "--cdf_file", help='component description file, default metadata/package.yml', default=None)
        group1 = parser.add_argument_group('idf file', 'Generate code using the specified IDF file')
        group1.add_argument("-i", "--idf_file", help='A IDF file to be processed e.g.: com.litebmc.Upgrade.xml', default=None)

        args = parser.parse_args(self.args)

        if args.cdf_file:
            if not os.path.isfile(args.cdf_file):
                raise ArgException(f"argument -c/--cdf_file: {args.cdf_file} not exist")
            configs = Helper.read_yaml(args.cdf_file, "codegen", [])
            # 为保障兼容，package.yml未指定版本号的，默认使用2，该版本配套lb_base/0.6.0版本，其LBProperty无set/get成员
            self.codegen_version = Helper.read_yaml(args.cdf_file, "codegen_version", 2)
            for cfg in configs:
                file = cfg.get("file")
                if file is None:
                    log.error("%s的自动代码生成配置不正确, 缺少file元素指定描述文件", args.cdf_file)
                    sys.exit(-1)
                if not file.endswith(".yaml") :
                    log.error("%s的自动代码生成配置不正确, %s的文件名不是以.yaml结束", args.cdf_file, file)
                    sys.exit(-1)
                if not os.path.isfile(file):
                    log.error("%s的自动代码生成配置不正确, %s不是一个文件", args.cdf_file, file)
                    sys.exit(-1)
                outdir = cfg.get("outdir", os.getcwd())
                self._gen(file, outdir)
            return

        intf_file = args.idf_file
        if not intf_file:
            raise ArgException(f"argument error, arguments -c/--cdf_file and -i/--idf_file are not set")
        if not os.path.isfile(intf_file):
            raise ArgException(f"argument -i/--idf_file: {args.idf_file} not exist")
        if args.codegen_version > __version__ or args.codegen_version <= 0:
            raise ArgException(f"argument -v/--codegen_version: validate failed, must less than or equal to {__version__} and bigger than 0")
        self.codegen_version = args.codegen_version
        out_dir = os.path.join(os.getcwd(), args.directory)
        if not intf_file.endswith(".yaml"):
            raise ArgException(f"The IDF file ({intf_file}) not endswith .yaml")
        if  not os.path.isfile(intf_file):
            raise ArgException(f"The IDF file ({intf_file}) not exist")
        if not os.path.isdir(out_dir):
            log.warning(f"Directory {args.directory} not exist, try create")
            os.makedirs(out_dir)
        self._gen(intf_file, out_dir)

if __name__ == "__main__":
    gen = CodeGen(sys.argv)
    gen._gen("com.litebmc.test.xml", ".")

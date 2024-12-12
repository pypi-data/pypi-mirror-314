"""任务基础类"""
import os
import json
import tempfile
from queue import Queue
from threading import Thread
from lbkit.log import Logger
from lbkit.errors import LiteBmcException
from lbkit import misc
from lbkit.tools import Tools

tools = Tools("comp_build")
log = Logger("comp_build")

class ConanPackage():
    def __init__(self, node):
        self.node = node
        self.deps: dict[str, ConanPackage] = {}
        self.build_deps: dict[str, ConanPackage] = {}
        self.ref = node.get("ref")
        self.pkg = self.ref.split("#")[0]
        self.name = self.pkg.split("/")[0]
        self.context = node.get("context")
        self.building = False
        self.is_host = self.context == "host"
        binary = node.get("binary")
        self.binary_exist = (binary in ["Cache"])

    def append_dep(self, dep):
        self.deps[dep.pkg] = dep

    def append_build_dep(self, dep):
        self.build_deps[dep.pkg] = dep

    # 间接构建依赖更新为直接依赖
    def update_indirect_build_dep(self):
        deps = {}
        for _, dep in self.build_deps.items():
            sub_deps = dep.update_indirect_build_dep()
            deps.update(sub_deps)
        self.build_deps.update(deps)
        return self.build_deps

    @property
    def options(self):
        return self.node.get("options", {})

    @property
    def settings(self):
        return self.node.get("settings", {})

    @property
    def default_options(self):
        return self.node.get("default_options", {})


class BuildConanParallel(object):
    def __init__(self, graphinfo, lockfile, cmd, force_build):
        self.queue = Queue()
        self.cmd = ""
        chunks = cmd.split()
        skip = False
        for chunk in chunks:
            if skip:
                skip = False
                continue
            if chunk in ["--user", "--channel", "--version", "--name"]:
                skip = True
                continue
            self.cmd += f"{chunk} "
        self.graphinfo = os.path.realpath(graphinfo)
        self.lockfile = os.path.realpath(lockfile)
        if not os.path.isfile(graphinfo):
            raise LiteBmcException(f"graph file {graphinfo} not exist")
        self.exception = None
        self.force_build = force_build

    def build_dep(self, cp: ConanPackage, options):
        for name, value in cp.settings.items():
            options += f" -s {name}={value}"

        cmd = f"conan install --requires={cp.ref} {self.cmd} {options}"
        if self.force_build:
            cmd += f" --build=\"{cp.name}/*\""
        cmd += " --build=missing"
        cmd += f" --lockfile={self.lockfile}"
        try:
            logfile = f"{misc.LOG_DIR}/conan_{cp.name}.log"
            log.info(f">>>> build {cp.ref} start, logfile: {logfile}")
            log.debug(f">>>> {cmd}")
            tools.exec(cmd, echo_cmd=False, log_name=logfile)
            log.success(f"<<<< build {cp.ref} finished")
        except Exception as e:
            self.exception = e
        self.queue.put(cp)

    def _build(self):
        with open(self.graphinfo, "r") as fp:
            grapth = json.load(fp)
        nodes = grapth.get("graph", {}).get("nodes", {})
        packages: dict[str, ConanPackage] = {}

        build_works = {}
        for id, node in nodes.items():
            if id == "0":
                continue
            cp = ConanPackage(node)
            packages[cp.pkg] = cp
            build_works[cp.name] = False
        for id, node in nodes.items():
            if id == "0":
                continue
            ref = node.get("ref")
            if ref.startswith("litebmc/"):
                continue
            cp = packages[ref.split("#")[0]]
            deps = node.get("dependencies", {})
            for _, dep in deps.items():
                dep_ref = dep.get("ref")
                direct = dep.get("direct")
                if not direct:
                    continue
                dep_cp = packages[dep_ref]
                if dep_cp.is_host:
                    cp.append_dep(dep_cp)
                else:
                    cp.append_build_dep(dep_cp)
        options = ""
        for _, cp in packages.items():
            for name, value in cp.options.items():
                if value is None:
                    continue
                def_val = cp.default_options.get(name)
                conan_name = cp.pkg.split("@")[0]
                if isinstance(def_val, bool):
                    if (def_val and "False" == value) or (not def_val and "True" == value):
                        options += f" -o {conan_name}:{name}={value}"
                elif def_val != value:
                    options += f" -o {conan_name}:{name}={value}"
        # 工具间接依赖变更为直接依赖
        for name, pkg in packages.items():
            pkg.update_indirect_build_dep()
        wait_finished = 0
        while True:
            for _, cp in packages.items():
                if wait_finished >= 4:
                    continue
                if cp.ref.startswith("litebmc/"):
                    continue
                # 如果是构建工具，不参与构建
                if not cp.is_host:
                    continue
                # 如果还有依赖未构建完成，不参与构建
                if len(cp.deps) != 0:
                    continue
                # 如果正在构建
                if cp.building:
                    continue
                # 相同名称的组件正在构建时不启动新的构建
                if build_works[cp.name]:
                    continue
                if not cp.binary_exist or self.force_build:
                    # 当依赖的构建工具存在正在构建的组件时不能构建
                    need_build = True
                    for _, dep in cp.build_deps.items():
                        # 正在构建且未构建出制品时
                        if not dep.binary_exist and dep.building:
                            need_build = False
                            break
                    if not need_build:
                        continue
                    cp.building = True
                    # 启动构建前将其依赖的构建工具置为正在构建
                    for _, dep in cp.build_deps.items():
                        dep.building = True
                    build_works[cp.name] = True
                    wait_finished += 1
                    thread = Thread(target=self.build_dep, args=(cp, options,))
                    thread.start()
                else:
                    cp.building = True
                    build_works[cp.name] = True
                    wait_finished += 1
                    self.queue.put(cp)
            if not wait_finished:
                return
            cp = self.queue.get()
            if self.exception:
                raise self.exception
            build_works[cp.name] = False
            wait_finished -= 1
            for _, sub_cp in packages.items():
                if sub_cp.deps.get(cp.pkg):
                    sub_cp.deps.pop(cp.pkg)
            # 构建完成后，组件的构建依赖工具一定构建完成且制品存在
            for _, dep in cp.build_deps.items():
                dep.building = False
                dep.binary_exist = True


    def build(self):
        cwd = os.getcwd()
        tmp = tempfile.TemporaryDirectory()
        os.chdir(tmp.name)
        self._build()
        os.chdir(cwd)

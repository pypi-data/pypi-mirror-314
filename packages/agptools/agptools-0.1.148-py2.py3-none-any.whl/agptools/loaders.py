"""
A basic dynamic module loader
"""

import importlib
import re
import os
import traceback
import sys
from typing import List
import yaml
import pickle
import hashlib

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------

from .helpers import BASEOF, NAMEOF

# from agptools.logs import logger

# log = logger(__name__)

# subloger = logger(f'{__name__}.subloger')
# import jmespath


def load_yaml(path):
    if os.path.exists(path):
        return yaml.load(open(path, encoding="utf-8"), Loader=yaml.Loader)
    return {}


def save_yaml(data, path, force=True):  # TODO: force=False
    if force or not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        yaml.dump(data, open(path, "wt", encoding="utf-8"), Dumper=yaml.Dumper)
    return yaml.load(open(path, encoding="utf-8"), Loader=yaml.Loader)


# ----------------------------------------------------------
# Dynamic Loaders
# ----------------------------------------------------------


class Finder:
    CACHE = {}
    HANDLERS = {}
    SKIP = set(
        [
            "ctypes",
        ]
    )

    @staticmethod
    def blueprint(meta):
        """Create a blueprint for a meta search criteria"""
        keys = list(meta.keys())
        keys.sort()
        data = [(k, meta[k]) for k in keys]
        blue = pickle.dumps(data)
        blue = hashlib.md5(blue).hexdigest()
        return blue

    @staticmethod
    def mach(item, meta) -> bool:

        for key, value in meta.items():
            function = Finder.HANDLERS.get(key)
            if function:
                try:
                    if not function(item, value):
                        return False
                except Exception:
                    return False

        return True

    @classmethod
    def find_in_memory(cls, modules: List | str, force=False, **meta):
        if not force:
            blueprint = cls.blueprint(meta)
            result = cls.CACHE.get(blueprint)
            if result:
                return result

        result = []
        visited = set()
        if isinstance(modules, str):
            modules = [modules]
        while missing := visited.symmetric_difference(sys.modules):
            for module_fqid in missing:
                if module_fqid in visited:
                    continue
                visited.add(module_fqid)
                # print(f"? {module_fqid}")
                if module_fqid in cls.SKIP:
                    continue
                for pattern in modules:
                    if re.match(pattern, module_fqid):
                        break
                else:
                    continue

                # print(f"--> OK: {module_fqid}")

                module = sys.modules.get(module_fqid)
                if not module:
                    continue

                for name in dir(module):
                    try:
                        item = getattr(module, name)
                    except Exception:
                        continue

                    if cls.mach(item, meta):
                        # not sure we can use set() instead list()
                        if item not in result:
                            result.append(item)
                break  # rebuilt missing

        cls.CACHE[blueprint] = result

        return result


# Populate handlers
Finder.HANDLERS["name"] = NAMEOF
# Finder.HANDLERS["klass"] = lambda item, value: isinstance(item, value)
Finder.HANDLERS["klass"] = BASEOF


def mro(item, value):
    if isinstance(value, str):
        for layer in item.mro():
            if value in str(layer):
                return True
        return False
    return value in item.mro()


Finder.HANDLERS["mro"] = mro


class ModuleLoader:
    """A minimal module loader class"""

    ACTIVE_PORT_KEY = "active_ports"

    @classmethod
    def get_project_root(cls):
        for path in sys.path:
            r = __file__.split(path)
            if len(r) > 1:
                return path, r[1:]

    def __init__(self, top):
        self.root, self.my_path = self.get_project_root()

        if not isinstance(top, str):
            # should be a module
            top = os.path.dirname(top.__file__)
        if os.path.isfile(top):
            top = os.path.dirname(top)
        self.top = top
        self.active_ports = [".*"]
        self.load_config()

    def load_config(self, path="config.yaml"):
        for _path in self.find(type_="f", name=path):
            try:
                cfg = yaml.load(open(_path, encoding="utf-8"), Loader=yaml.Loader)
                self.active_ports = cfg.get(self.ACTIVE_PORT_KEY, self.active_ports)
            except Exception as why:
                print(f"ERROR loading {_path}: {why}")
            break
        return self.active_ports

    @staticmethod
    def match_any_regexp(name, active_ports) -> bool:
        for regex in active_ports:
            if re.match(regex, name):
                return True
        return False

    def available_modules(self, active_ports=None) -> List[str]:
        names = []

        active_ports = active_ports or self.active_ports

        top = self.top
        for _root, _folders, _files in os.walk(top):
            for _name in _files:
                _name, _ext = os.path.splitext(_name)
                if _ext not in (".py",) or _name.startswith("__"):
                    continue
                _path = os.path.join(_root, _name)
                _path = _path.split(top)[-1].split(os.path.sep)[1:]
                _path = ".".join(_path)
                if self.match_any_regexp(_path, active_ports):
                    names.append(_path)

        names.sort()
        return names

    def load_modules(self, names):

        top = self.top
        # old = list(sys.path)
        # sys.path.insert(0, top)
        modules = []
        for name in names:
            name = f"{top}.{name}"
            name = name.split(self.root)[1][1:].replace("/", ".")
            try:
                print(f"Loading: {name}")
                mod = importlib.import_module(name)
                # mod = __import__(name)
                modules.append(mod)
            except ImportError as why:
                print(f"ERROR importing: {name}")
                print(why)
                info = traceback.format_exception(*sys.exc_info())
                print("".join(info))
        # sys.path = old
        return modules

    def find(self, type_=["d", "f"], name=".*"):
        "mimic unix `find` command"
        if not isinstance(type_, list):
            type_ = list(type_)

        for root, folders, files in os.walk(self.root):
            candidates = {
                "d": folders,
                "f": files,
            }
            for t in type_:
                for _name in candidates.get(t, []):
                    if re.match(name, _name):
                        yield os.path.join(root, _name)

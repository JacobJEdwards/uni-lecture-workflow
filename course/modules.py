#!/usr/bin/env python

import yaml
from config import (
    CURRENT_ROOT,
    CURRENT_COURSE_SYMLINK,
    CURRENT_COURSE_WATCH_FILE,
)
from course.lectures import Lectures


class Module:
    """Defines a module object"""

    def __init__(self, path) -> None:
        self.path = path
        self.name = path.stem
        with open(path / "info.yaml") as file:
            self.info = yaml.full_load(file)
        self.code = self.info["code"]
        self._lectures = Lectures(self)
        self.year_long = self.info["semester"] == "Year long"

    @property
    def lectures(self) -> Lectures | None:
        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        return self.path == other.path


class Modules(list):
    """Defines a list of modules"""

    def __init__(self) -> None:
        list.__init__(self, self.read_files())

    @staticmethod
    def read_files() -> list:
        module_dirs = [x for x in CURRENT_ROOT.iterdir() if x.is_dir()]
        _modules = [Module(path) for path in module_dirs]
        return sorted(_modules, key=lambda c: c.name)

    @property
    def current(self) -> Module | None:
        if not CURRENT_COURSE_SYMLINK.exists():
            return None
        return Module(CURRENT_COURSE_SYMLINK.resolve())

    @current.setter
    def current(self, module: Module) -> None:
        if CURRENT_COURSE_SYMLINK.exists():
            CURRENT_COURSE_SYMLINK.unlink()
        CURRENT_COURSE_SYMLINK.symlink_to(module.path)
        CURRENT_COURSE_WATCH_FILE.write_text(f"{module.info['short']}\n")

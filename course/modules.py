#!/usr/bin/env python

import yaml
from config import (
    CURRENT_ROOT,
    CURRENT_COURSE_SYMLINK,
    CURRENT_COURSE_WATCH_FILE,
)
from course.lectures import Lectures


class Module:
    def __init__(self, path):
        self.path = path
        self.name = path.stem

        self.info = yaml.full_load((path / "info.yaml").open())
        self.code = self.info["code"]
        self._lectures = None
        self.year_long = self.info["semester"] == "Year long"

    @property
    def lectures(self) -> Lectures:
        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        return self.path == other.path


class Modules(list):
    def __init__(self):
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
    def current(self, module) -> None:
        if CURRENT_COURSE_SYMLINK.exists():
            CURRENT_COURSE_SYMLINK.unlink()
        CURRENT_COURSE_SYMLINK.symlink_to(module.path)
        CURRENT_COURSE_WATCH_FILE.write_text(f"{module.info['short']}\n")

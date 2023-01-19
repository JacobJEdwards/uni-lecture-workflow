#!/usr/bin/env python

from pathlib import Path
from config import YEAR_LONG_ROOT, DATE_FORMAT, SUBMODULES
from course.modules import Modules
from datetime import date


def addDirectories(module) -> None:
    for sub in SUBMODULES:
        Path(module.path / sub).mkdir(parents=True, exist_ok=True)


def addMaster(module) -> None:
    course_title: str = module.info["title"]

    lines = [
        r"\documentclass[a4paper, titlepage]{article}",
        r"\input{../../../preamble.tex}",
        rf"\title{{{course_title}}}",
        rf"\date{{{date.today().strftime(DATE_FORMAT)}}}",
        r"\begin{document}",
        r"    \maketitle",
        r"    \tableofcontents",
        rf"    % start lectures",
        rf"    % end lectures",
        r"\end{document}",
    ]
    master = module.lectures.master_tex
    if not master.exists():
        master.touch()
        master.write_text("\n".join(lines))


def addYearLongs(module) -> None:
    # creates submodule directory and subdirectories
    Path(YEAR_LONG_ROOT / module.name / "Lectures").mkdir(parents=True, exist_ok=True)
    Path(YEAR_LONG_ROOT / module.name / "Seminars").mkdir(parents=True, exist_ok=True)
    Path(YEAR_LONG_ROOT / module.name / "Labs").mkdir(parents=True, exist_ok=True)
    Path(YEAR_LONG_ROOT / module.name / "Assessments").mkdir(
        parents=True, exist_ok=True
    )


def main() -> None:
    for module in Modules():
        addDirectories(module)
        addMaster(module)

        if module.year_long:
            addYearLongs(module)


if __name__ == "__main__":
    main()

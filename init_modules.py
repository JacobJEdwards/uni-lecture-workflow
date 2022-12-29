#!/usr/bin/env python

from course.modules import Modules
import os
from config import YEAR_LONG_ROOT


def addDirectories(module):
    os.makedirs(module.path / 'Lectures' / 'figures', exist_ok=True)
    os.makedirs(module.path / 'Lectures' / 'TeX', exist_ok=True)
    
    os.makedirs(module.path / 'Labs', exist_ok=True)
    os.makedirs(module.path / 'Seminars', exist_ok=True)
    os.makedirs(module.path / 'Assessments', exist_ok=True)

def addMaster(module):
    course_title: str = module.info["title"]

    lines = [r'\documentclass[a4paper]{article}',
                 r'\input{../../preamble.tex}',
                 fr'\title{{{course_title}}}',
                 r'\begin{document}',
                 r'    \maketitle',
                 r'    \tableofcontents',
                 fr'    % start lectures',
                 fr'    % end lectures',
                 r'\end{document}'
            ]

def addYearLongs(module):
    # creates sub module directory and subdirectories
    os.makedirs(YEAR_LONG_ROOT / module.name / 'Lectures', exist_ok=True)
    os.makedirs(YEAR_LONG_ROOT / module.name / 'Seminars', exist_ok=True)
    os.makedirs(YEAR_LONG_ROOT / module.name / 'Labs', exist_ok=True)




def main():    
    for module in Modules():
        addDirectories(module)
        addMaster(module)

        if module.year_long:
            addYearLongs(module)


if __name__ == '__main__':
    main()

#!/usr/bin/env python

import os
from pathlib import Path
from datetime import datetime
import frontmatter

from config import ROOT, CURRENT_COURSE_SYMLINK, CURRENT_ROOT, DATE_FORMAT

def filename2number(filename) -> int:
    return int(str(filename).replace('.md', '')
                            .replace('.tex', '')
                            .replace('.pdf', '')
                            .replace('lec_', '')
                            .replace('.markdown', ''))

def number2filename(number, type='md') -> str:
    return f"lec_{number:02d}.{type}"


class Lecture():
    def __init__(self, path, module):
        self.info = frontmatter.load(path)

        date = self.info['date']
        
        self.date = datetime.strptime(date, DATE_FORMAT)
        self.number = filename2number(path.stem)

        self.module = module
        self.path = path

        self.title = self.info['title']
        self.file_type = path.suffix

    def __str__(self):
        return f'<{self.module.info["short"]} Lecture {self.number}: {self.title}>'


class Lectures(list):
    def __init__(self, module):
        self.module = module
        self.root = module.path / 'Lectures'
        self.master_tex = self.root / 'master.tex'
        list.__init__(self, self.read_files())

    def read_files(self) -> list:
        files = self.root.glob('lec_*.md')
        _lectures = (Lecture(path, self.module) for path in files)
        return sorted(_lectures, key=lambda x: x.number)

    def new_markdown(self):
        number = len(self) + 1
        filename = number2filename(number)
        path = self.root / filename
        with open(path) as f:
            f.write(f"""---
                        title: 
                        module: {self.module.info['title']}
                        date: {datetime.now().strftime(DATE_FORMAT)}
                        ---
                    """)


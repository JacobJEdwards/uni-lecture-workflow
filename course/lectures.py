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

        self.date = self.info['date']
        
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
    
    @staticmethod
    def get_start_end(filepath):
        start = None
        end = None
        with open(filepath) as f:
            for line in f:
                if 'lecture start' in line:
                    start = line
                if 'lecture end' in line:
                    end = line
        
        return start, end
    
    def update_master(self, num):
        start, end = self.get_start_end(self.master_tex)
        with open(self.master_tex) as f:
            lines = f.readlines()
        
        start_index = lines.index(start)
        end_index = lines.index(end)
        
        lecture = number2filename(num)

        new_lines = lines[:end_index-1]
        new_lines.append(f'\\markdownInput{{{lecture}}}')


    def new_markdown(self):
        print(f'len = {len(self)}')
        if len(self) != 0:
            new_lecture_number = self[-1].number + 1
        else:
            new_lecture_number = 1

        filename = number2filename(new_lecture_number)
        path = self.root / filename
        path.touch()
        module = self.module.info['title']
        lines = [
                    f'---',
                    f'title: ',
                    f'module: {module}',
                    f'date: {datetime.now().strftime(DATE_FORMAT)}',
                    f'---',
                ]

        path.write_text('\n'.join(lines))
        #self.update_master(new_lecture_number)
        self.read_files()




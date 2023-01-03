#!/usr/bin/env python

from datetime import datetime
import frontmatter
from config import DATE_FORMAT


def filename2number(filename) -> int:
    return int(
        str(filename)
        .replace(".md", "")
        .replace(".tex", "")
        .replace(".pdf", "")
        .replace("lec_", "")
        .replace(".markdown", "")
    )


def number2filename(number, file_type="md") -> str:
    return f"lec_{number:02d}.{file_type}"


class Lecture:
    def __init__(self, path, module):
        self.info = frontmatter.load(path)

        self.date = self.info["date"]

        self.number = filename2number(path.stem)

        self.module = module
        self.path = path

        self.title = self.info["title"]
        self.file_type = path.suffix

    def __str__(self) -> str:
        return f'<{self.module.info["short"]} Lecture {self.number}: {self.title}>'


class Lectures(list):
    def __init__(self, module):
        self.module = module
        self.root = module.path / "Lectures"
        self.master_tex = self.root / "master.tex"
        list.__init__(self, self.read_files())

    def read_files(self) -> list:
        files = self.root.glob("lec_*.md")
        _lectures = (Lecture(path, self.module) for path in files)
        return sorted(_lectures, key=lambda x: x.number)

    @staticmethod
    def get_start_end(filepath) -> tuple:
        start = None
        end = None
        with open(filepath) as f:
            lines = f.readlines()

        for line in lines:
            if "% start lectures" in line:
                start = lines.index(line)
            if "% end lectures" in line:
                end = lines.index(line)

        return start, end

    def update_master(self, num) -> None:
        start_index, end_index = self.get_start_end(self.master_tex)

        with open(self.master_tex) as f:
            lines = f.readlines()

        lines[start_index + 1 : end_index] = "".join(
            " " * 4 + r"\markdownInput{" + number2filename(number) + "}\n"
            for number in range(1, num + 2)
        )

        with open(self.master_tex, "w") as f:
            f.write("".join(lines))

    def new_markdown(self) -> Lecture:
        if len(self) != 0:
            new_lecture_number = self[-1].number + 1
        else:
            new_lecture_number = 1

        filename = number2filename(new_lecture_number)
        path = self.root / filename
        path.touch()
        module = self.module.info["title"]
        lines = [
            f"---",
            f"title: ",
            f"module: {module}",
            f"date: {datetime.now().strftime(DATE_FORMAT)}",
            f"---",
        ]

        path.write_text("\n".join(lines))

        self.read_files()
        self.update_master(len(self))

        return Lecture(path, self.module)

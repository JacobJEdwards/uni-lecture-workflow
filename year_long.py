#!/usr/bin/env python

from pathlib import Path
from course.modules import Modules
from config import YEAR_LONG_ROOT

# iterates through each module
for module in Modules():
    # does nothing if the module is not year long
    if not module.year_long:
        continue

    # iterates through each file in the year long module directory
    for dir in module.path.iterdir():
        if dir.is_file():
            continue

        event_type = dir.stem
        # symlinks each new file in year long module to correct folder in year long directory
        for file in dir.iterdir():
            if Path(YEAR_LONG_ROOT / module.name / event_type / file.name).exists():
                continue

            Path(YEAR_LONG_ROOT / module.name / event_type / file.name).symlink_to(file)



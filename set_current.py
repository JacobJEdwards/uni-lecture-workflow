from calender.events import next_event
from pathlib import Path
from config import COURSES
from course.modules import Modules
import yaml

def main():
    event: dict = next_event(1)
    if not event:
        exit()

    summary: str = event['summary']
    
    for module in Modules():
        if module.code == summary:
            
            if Modules().current is not None:
                if Modules().current == module:
                    exit()

            Modules().current = module
            module.lectures.new_markdown()
            break

if __name__ == '__main__':
    main()

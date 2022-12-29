from calender.events import next_event
from config import COURSES
from course.modules import Modules

def main():
    event: dict = next_event(1)
    if not event:
        exit()

    summary: str = event['summary']

    for module in Modules():
        if module.code == summary:
            Modules().current = module
            break

if __name__ == '__main__':
    main()

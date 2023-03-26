#!/usr/bin/env python

from calender.events import next_event
from course.modules import Modules


def main() -> None:
    event: dict = next_event(1)
    if not event:
        exit()

    print(event)

    summary: str = event["summary"]
    event_type: str = event["description"]

    for module in Modules():
        if module.code == summary:
            if Modules().current is not None:
                if Modules().current == module:
                    exit()

            Modules().current = module
            if "LECTURE" in event_type:
                module.lectures.new_markdown()
            break


if __name__ == "__main__":
    main()

#!/usr/bin/env python

from pathlib import Path
from datetime import datetime


def get_week(d=datetime.today()):
    return (int(d.strftime("%W")) + 52 - 5) % 52


DATE_FORMAT = "%Y-%m-%d"

CALENDAR_ID = "pdqsjtaoo91ft7tfj3pof0ir7u3633k9@import.calendar.google.com"
CREDENTIALS_FILE: str = str(
    Path("~/University/scripts/calender/client_secret.json").expanduser()
)

ROOT = Path("~/University").expanduser()
CURRENT_ROOT = ROOT / "Year1/Semester1"

CURRENT_COURSE_SYMLINK = ROOT / "CurrentModule"
CURRENT_COURSE_ROOT = CURRENT_COURSE_SYMLINK.resolve()
CURRENT_COURSE_WATCH_FILE = Path("/tmp/current_module").resolve()

YEAR_LONG_ROOT = ROOT / "Year1/YearLong"

COURSES: dict = {
    "CMP-4005Y": "Mathematics",
    "CMP-4011A": "WebDev",
    "CMP-4013A": "SysDev",
    "CMP-4008Y": "Programming",
    "CMP-4010B": "DatabaseSystems",
    "CMP-4002B": "ComputingPrinciples",
}

EVENTS: dict = {"LECTURE": "Lectures", "IT LABORATORY": "Labs", "SEMINAR": "Seminars"}

#!/usr/bin/env python

import datetime
from calender.setup import get_calendar_service
from config import CALENDAR_ID


def next_event(num: int) -> dict:
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            maxResults=num,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    if not events:
        return dict({})
    for event in events:
        time = event["start"].get("dateTime", event["start"].get("date"))
        summary = event["summary"]
        description = event["description"]
        return dict(time=time, summary=summary, description=description)

    return dict({})

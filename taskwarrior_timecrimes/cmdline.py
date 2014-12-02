from __future__ import print_function

import datetime

from pytz import utc

from .undo_reader import UndoReader


def cmdline():
    # No options for now
    since = (
        datetime.datetime.utcnow().replace(tzinfo=utc)
        - datetime.timedelta(hours=24)
    )
    reader = UndoReader(since=since)
    events = reader.get_available_events()

    for idx, event_date in enumerate(events):
        print("{idx}) {item}".format(
            idx=idx,
            item=event_date,
        ))
        for action in reader.get_event(event_date):
            if not action.get('is_old') and action.get('parent'):
                print(" - Added %s" % action['description'])

    print("")
    selection = raw_input(
        "Please select a recurrence to undo or press CTRL+C to quit: "
    )
    event = reader.get_event(events[int(selection)])

    print("")
    print("Execute the following command:")
    uuids = []
    for action in event:
        if action.get('is_old'):
            continue
        if not action.get('parent'):
            continue
        uuids.append(action['uuid'])
    print("")
    print(
        "  task rc.confirmation=no %s delete" % (
            ' '.join(uuids)
        )
    )
    print("")
    print(
        " - Answer 'Yes' when asked if you would "
        "like to permanently delete each task."
    )
    print(
        " - Answer 'No' when asked if you would like "
        "to delete all pending occurrences of each task."
    )

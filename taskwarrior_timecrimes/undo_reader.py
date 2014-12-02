import datetime
import os
import re

from taskw.warrior import TaskWarriorShellout

from dateutil.tz import tzlocal


class UndoReader(object):
    def __init__(self, since=None):
        self.client = TaskWarriorShellout()
        self.path = os.path.join(
            os.path.expanduser(self.client.config['data']['location']),
            'undo.data'
        )
        self.since = since
        self._document = self._read_document()

    def get_field_from_data(self, field, data):
        result = re.search('%s:"([^"]+)"' % field, data)
        if result:
            return result.group(1)

    def get_event(self, date):
        return self._document[date]

    def get_available_events(self):
        return self._document.keys()

    def _read_document(self):
        tasks = {}
        task = {}
        date = None
        should_record = True

        with open(self.path, 'r+') as f:
            for raw_line in f:
                line = raw_line.strip()
                if line == '---':
                    if should_record:
                        tasks[date].append(task)
                        task = {}
                    should_record = True
                if line.startswith('time'):
                    _, stamp = line.split(' ', 1)

                    date = (
                        datetime.datetime.fromtimestamp(float(stamp))
                    ).replace(tzinfo=tzlocal())
                    if self.since and date < self.since:
                        should_record = False
                    elif date not in tasks:
                        tasks[date] = []
                if line.startswith('old'):
                    task['is_old'] = True
                if line.startswith('new'):
                    _, data = line.split(' ', 1)
                    task['uuid'] = self.get_field_from_data('uuid', data)
                    task['description'] = (
                        self.get_field_from_data('description', data)
                    )
                    task['status'] = self.get_field_from_data('status', data)
                    parent = self.get_field_from_data('parent', data)
                    if parent:
                        task['parent'] = parent

        return tasks

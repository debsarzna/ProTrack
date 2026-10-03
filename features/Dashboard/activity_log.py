class ActivityLog:
    def __init__(self):
        self._entries = []

    def add(self, action, target, details):
        # newest first, so the table shows the latest activity at the top
        self._entries.insert(0, (action, target, details))

    def recent(self, limit=10):
        return self._entries[:limit]


activity_log = ActivityLog()
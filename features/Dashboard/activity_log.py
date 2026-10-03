class ActivityLog:
    def __init__(self):
        self.database = None

    def setup(self, database) -> None:
        self.database = database
        with self.database.connect() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    target TEXT NOT NULL,
                    details TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add(self, action, target, details) -> None:
        with self.database.connect() as con:
            con.execute(
                "INSERT INTO activity_log (action, target, details) VALUES (?, ?, ?)",
                (action, target, str(details)),
            )

    def recent(self, limit=10):
        with self.database.connect() as con:
            rows = con.execute(
                """
                SELECT action, target, details,
                       strftime('%H:%M', created_at, 'localtime')
                FROM activity_log
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [tuple(row) for row in rows]


activity_log = ActivityLog()
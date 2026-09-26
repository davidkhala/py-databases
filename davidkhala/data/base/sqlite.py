import sqlite3
from typing import Any

from davidkhala.data.base import Connectable


class SQLite(Connectable):
    def __init__(self, path: str = ":memory:"):
        super().__init__()
        self.path = path

    def connect(self) -> bool:
        self.connection: sqlite3.Connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        return True

    def query(
        self,
        template: str,
        values: dict | None = None,
    ) -> sqlite3.Cursor:
        return self.connection.execute(template, values or {})

    @staticmethod
    def rows_to_dicts(result: sqlite3.Cursor) -> list[dict[str, Any]]:
        return [dict(row) for row in result.fetchall()]

    def scalar(self, template: str, values: dict | None = None) -> Any:
        row = self.query(template, values).fetchone()
        assert len(row) == 1
        return row[0]
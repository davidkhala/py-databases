import unittest

from davidkhala.data.base.sqlite import SQLite


class SQLiteTestCase(unittest.TestCase):

    def setUp(self):
        self.db = SQLite()  # :memory:
        self.db.connect()
        self.db.query("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        self.db.query(
            "INSERT INTO users VALUES (:id, :name, :age)",
            {"id": 1, "name": "Alice", "age": 30}
        )
        self.db.query(
            "INSERT INTO users VALUES (:id, :name, :age)",
            {"id": 2, "name": "Bob", "age": 25}
        )

    def tearDown(self):
        self.db.close()

    def test_context_manager(self):
        with SQLite() as db:
            db.query("CREATE TABLE t (x INTEGER)")
            db.query("INSERT INTO t VALUES (:x)", {"x": 42})
            result = db.query("SELECT x FROM t")
            rows = SQLite.rows_to_dicts(result)
        self.assertEqual(rows, [{"x": 42}])

    def test_query_and_rows_to_dicts(self):
        result = self.db.query("SELECT id, name, age FROM users ORDER BY id")
        rows = SQLite.rows_to_dicts(result)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], {"id": 1, "name": "Alice", "age": 30})
        self.assertEqual(rows[1], {"id": 2, "name": "Bob", "age": 25})

    def test_query_with_values(self):
        result = self.db.query("SELECT name FROM users WHERE id = :id", {"id": 2})
        rows = SQLite.rows_to_dicts(result)
        self.assertEqual(rows, [{"name": "Bob"}])

    def test_scalar(self):
        count = self.db.scalar("SELECT COUNT(*) FROM users")
        self.assertEqual(count, 2)

    def test_scalar_with_values(self):
        age = self.db.scalar("SELECT age FROM users WHERE id = :id", {"id": 1})
        self.assertEqual(age, 30)

    def test_scalar_asserts_single_column(self):
        with self.assertRaises(AssertionError):
            self.db.scalar("SELECT id, name FROM users WHERE id = :id", {"id": 1})


if __name__ == "__main__":
    unittest.main()

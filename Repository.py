import atexit
import sqlite3
import sys

from DAO import _Hats, _Orders, _Suppliers


class _Repository:
    def __init__(self, db_name):
        self._conn = sqlite3.connect(db_name)
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        # db_cursor.execute(
        #     "CREATE TABLE hats(ID INTEGER PRIMARY KEY,topping VARCHAR NOT NULL, supplier INTEGER REFERENCES Supplier(id), quantity INTEGER NOT NULL);")
        # db_cursor.execute("CREATE TABLE suppliers(ID INTEGER PRIMARY KEY,name VARCHAR NOT NULL);")
        # db_cursor.execute(
        #     "CREATE TABLE orders(ID INTEGER PRIMARY KEY,location VARCHAR NOT NULL, hat INTEGER REFERENCES hats(id));")
        self._conn.executescript("""
        CREATE TABLE students (
            id      INT         PRIMARY KEY,
            name    TEXT        NOT NULL
        );

        CREATE TABLE assignments (
            num                 INT     PRIMARY KEY,
            expected_output     TEXT    NOT NULL
        );

        CREATE TABLE grades (
            student_id      INT     NOT NULL,
            assignment_num  INT     NOT NULL,
            grade           INT     NOT NULL,

            FOREIGN KEY(student_id)     REFERENCES students(id),
            FOREIGN KEY(assignment_num) REFERENCES assignments(num),

            PRIMARY KEY (student_id, assignment_num)
        );
    """)


# the repository singleton
repo = _Repository(sys.argv[1])
atexit.register(repo._close)
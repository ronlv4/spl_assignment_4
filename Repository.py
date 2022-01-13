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
        self._conn.executescript("""
        CREATE TABLE hats (
            ID          INTEGER         PRIMARY KEY,
            topping     VARCHAR         NOT NULL,
            supplier    INTEGER         REFERENCES Supplier(id),
            quantity    INTEGER         NOT NULL
        );

        CREATE TABLE suppliers(
            ID          INTEGER         PRIMARY KEY,
            name        VARCHAR         NOT NULL
        );

        CREATE TABLE orders (
            ID          INTEGER         PRIMARY KEY,
            location    VARCHAR         NOT NULL,
            hat         INTEGER         REFERENCES hats(ID)
        );
    """)


# the repository singleton
repo = _Repository(sys.argv[1])
atexit.register(repo._close)

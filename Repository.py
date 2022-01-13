import atexit
import sqlite3
import sys
import os

from DAO._Hats import _Hats
from DAO._Orders import _Orders
from DAO._Suppliers import _Suppliers


class HatWithSupplier:
    def __init__(self, hat_id, hat_quantity, supplier_name):
        self.hat_id = hat_id
        self.hat_quantity = hat_quantity
        self.supplier_name = supplier_name


class _Repository:
    def __init__(self, db_name):
        self.db_already_existed = os.path.isfile(db_name)
        self._conn = sqlite3.connect(db_name)
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        if self.db_already_existed:
            return False
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
            hat         INTEGER         REFERENCES hats(id)
            );
        """)
        return True

    def get_hat_with_supplier(self, topping):
        c = self._conn.cursor()
        one = c.execute(
            f'SELECT hats.ID, hats.quantity, suppliers.name from hats JOIN suppliers ON hats.supplier=suppliers.ID WHERE hats.topping="{topping}" ORDER BY suppliers.ID ASC').fetchone()
        return HatWithSupplier(*one)


# the repository singleton
repo = _Repository(sys.argv[4])
atexit.register(repo._close)

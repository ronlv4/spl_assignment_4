import atexit
import sqlite3
import sys
from DAO._Hats import _Hats
from DAO._Suppliers import _Suppliers
from DAO._Orders import _Orders
from DTO.Order import Order


class _Repository:
    def __init__(self, db_name):
        self._conn = sqlite3.connect(db_name)
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def _execute(self, topping):
        orderid = self.hats.findIdForOrder(topping)
        self.hats.update(orderid)
        return orderid

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE hats (
            id         INT     PRIMARY KEY,
            topping    TEXT    NOT NULL,
            supplier   INT     NOT NULL,
            quantity   INT     NOT NULL,
            
            FOREIGN KEY(supplier)  REFERENCES supplier(id),
        );

        CREATE TABLE supplier (
            id        INT     PRIMARY KEY,
            name      TEXT    NOT NULL
        );

        CREATE TABLE order (
            id        INT     PRIMARY KEY,
            location  TEXT    NOT NULL,
            hat       TEXT    NOT NULL,

            FOREIGN KEY(hat) REFERENCES hat(id),
        );
    """)

    def new_order(self, city, topping, order_id):
        id_for_order = self.hats.find_sup_topping(topping)
        self.hats.update_inventory(id_for_order)
        repo.orders.insert(Order(order_id, city, id_for_order))
        c = self._conn.cursor()
        c.execute("""SELECT hats.topping, suppliers.name, b.location FROM ((SELECT hat, location FROM orders WHERE id =
         ? ) AS b JOIN hats ON hats.id=b.hat) AS a JOIN suppliers ON a.supplier=suppliers.id""", [order_id])
        repo.hats.delete()
        return c.fetchone()

# the repository singleton
repo = _Repository(sys.argv[1])
atexit.register(repo._close)

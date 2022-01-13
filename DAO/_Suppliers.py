from DTO import Supplier


class _Suppliers:
    def __init__(self, db_con):
        self.db_con = db_con

    def insert(self, supplier):
        self.db_con.execute("INSERT INTO suppliers(id, name) VALUES (?,?)",
                            [supplier.id, supplier.name])

    def find(self, supplier_id):
        c = self.db_con.cursor()
        c.execute("SELECT id, name FROM hats WHERE id = ?", [supplier_id])
        return Supplier(*c.fetchone())



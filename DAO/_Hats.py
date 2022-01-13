from DTO import Hat


class _Hats:
    def __init__(self, db_con):
        self.db_con = db_con

    def insert(self, hat):
        self.db_con.execute("INSERT INTO hats(id, topping, supplier, quantity) VALUES (?,?,?,?)",
                            [hat.id, hat.topping, hat.supplier, hat.quantity])

    def find(self, hat_id):
        c = self.db_con.cursor()
        c.execute("SELECT id, topping, supplier, quantity FROM hats WHERE id = ?", [hat_id])
        return Hat(*c.fetchone())

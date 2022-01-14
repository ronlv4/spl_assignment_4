from DTO import Hat


class _Hats:
    def __init__(self, db_con):
        self.db_con = db_con

    def insert(self, hat):
        self.db_con.execute("INSERT INTO hats(id, topping, supplier, quantity) VALUES (?,?,?,?)",
                            [hat.hatid, hat.topping, hat.supplier, hat.quantity])

    def find(self, hat_id):
        c = self.db_con.cursor()
        c.execute("SELECT id, topping, supplier, quantity FROM hats WHERE id = ?", [hat_id])
        return Hat(*c.fetchone())

    def delete(self):
        self._conn.execute("""DELETE FROM hats WHERE quantity = (?)""", [0])

    def find_sup_topping(self, topping):
        c = self.db_con.cursor()
        c.execute("""SELECT id FROM hats WHERE topping = ? ORDER BY supplier ASC LIMIT 1 """, [topping])
        return c.fetchone()[0]

    def update_inventory(self, id_to_update):
        c = self.db_con.cursor()
        c.execute("""SELECT quantity FROM hats WHERE id = ?""", [id_to_update])
        amount = int(c.fetchone()[0]) - 1
        self.db_con.execute("""UPDATE hats SET quantity = ? WHERE id = ?""", [amount, id_to_update])
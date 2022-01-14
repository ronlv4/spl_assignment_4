from DTO import Order


class _Orders:
    def __init__(self, db_con):
        self.db_con = db_con

    def insert(self, order):
        self.db_con.execute("""INSERT INTO hats(id, location, hat) VALUES (?,?,?)""",
                            [order.id, order.location, order.hat])

    def find(self, order_id):
        c = self.db_con.cursor()
        c.execute("""SELECT id, location, hat FROM hats WHERE id = ?""", [order_id])
        return Order(*c.fetchone())



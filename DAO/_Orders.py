from DTO import Order


class _Orders:
    def __init__(self, db_con):
        self.db_con = db_con

    def insert(self, order):
        self.db_con.execute("INSERT INTO hats(topping, location) VALUES (null,?,?)",
                            [order.topping, order.location])
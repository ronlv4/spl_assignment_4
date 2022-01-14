import sqlite3
import os
import sys
from DTO.Hat import Hat
from DTO.Order import Order
from DTO.Supplier import Supplier
from Repository import repo


# def populate_db_from_input(path, db_cursor):
#     with open(path, 'r') as f:
#         num_of_hats, num_of_suppliers = map(int, f.readline().split(','))
#         for iwndex, line in zip(range(num_of_hats), f):
#             row = tuple(line[:-1].split(','))
#             db_cursor.execute("INSERT INTO hats VALUES(?,?,?,?)", row)
#         for index, line in zip(range(num_of_suppliers), f):
#             row = tuple(line[:-1].split(',')) if line[-1] == '\n' else tuple(line.split(','))
#             db_cursor.execute("INSERT INTO suppliers VALUES(?,?)", row)


# def create_tables(db_cursor):
#     db_cursor.execute(
#         "CREATE TABLE hats(ID INTEGER PRIMARY KEY,topping VARCHAR NOT NULL, supplier INTEGER REFERENCES Supplier(id), quantity INTEGER NOT NULL);")
#     db_cursor.execute("CREATE TABLE suppliers(ID INTEGER PRIMARY KEY,name VARCHAR NOT NULL);")
#     db_cursor.execute(
#         "CREATE TABLE orders(ID INTEGER PRIMARY KEY,location VARCHAR NOT NULL, hat INTEGER REFERENCES hats(id));")
#

# def generate_orders(path):
#     with open(path, 'r') as f:
#         for line in f:
#             yield line[:-1].split(',') if line[-1] == '\n' else line.split(',')
#

# def execute_order(db_cursor, location, topping):
#     db_cursor.execute(f'SELECT hats.ID, hats.quantity, suppliers.name from hats JOIN suppliers ON hats.supplier=suppliers.ID WHERE hats.topping="{topping}" ORDER BY suppliers.ID ASC')
#     hat_id, current_topping_quantity, supplier = db_cursor.fetchone()
#     if current_topping_quantity == 1:
#         command = f'DELETE FROM hats WHERE ID = {hat_id}'
#     else:
#         command = f'UPDATE hats SET quantity = {int(current_topping_quantity) - 1} WHERE ID = {hat_id}'
#     db_cursor.execute(command)
#     db_cursor.execute(f'INSERT INTO orders VALUES(null,?,?)', (location, hat_id))
#     return supplier


def main():
    config_path = sys.argv[1]
    orders_path = sys.argv[2]
    output_path = sys.argv[3]
    db_name = sys.argv[4]
    db_already_existed = os.path.isfile(db_name)
    db_con = sqlite3.connect(db_name)
    repo.__init__()
    repo.create_tables()
    with open(config_path) as input_file:
        first_line = input_file.readline()
        amounts = first_line.split(',')
        num_hats = int(amounts[0])
        num_sups = int(amounts[1])
        for line in input_file:
            if num_hats > 0:
                cur = line.strip().split(',')
                repo.hats.insert(Hat(int(cur[0]), cur[1], int(cur[2]), int(cur[3])))
                num_hats -= 1
            elif num_sups > 0:
                cur = line.strip().split(',')
                repo.suppliers.insert(Supplier(int(cur[0]), cur[1]))
                num_sups -= 1
    cur_order_id = 1
    with open(orders_path) as input_file:
        for line in input_file:
            cur = line.strip().split(',')
            city = cur[0]
            topping = cur[1]
            cur_order = repo.new_order(city, topping, cur_order_id)
            open(output_path, "w+").write(cur_order[0]+","+cur_order[1]+","+cur_order[2]+"\n")


    # with db_con:
    #     cursor = db_con.cursor()
    #     if not db_already_existed:
    #         create_tables(cursor)
    #         populate_db_from_input(config_path, cursor)
    #     with open(output_path, 'w') as f:
    #         for location, topping in generate_orders(orders_path):
    #             supplier = execute_order(cursor, location, topping)
    #             f.write(','.join((topping, supplier, location)) + '\n')


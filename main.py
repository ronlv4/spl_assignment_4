import sqlite3

import os
import sys


def populate_db_from_input(path, db_cursor):
    with open(path, 'r') as f:
        num_of_hats, num_of_suppliers = map(int, f.readline().split(','))
        for index, line in zip(range(num_of_hats), f):
            row = tuple(line[:-1].split(','))
            db_cursor.execute("INSERT INTO hats VALUES(?,?,?,?)", row)
        for index, line in zip(range(num_of_suppliers), f):
            row = tuple(line[:-1].split(','))
            db_cursor.execute("INSERT INTO suppliers VALUES(?,?)", row)


def create_tables(db_cursor):
    cursor.execute("CREATE TABLE hats(ID INTEGER PRIMARY KEY,topping VARCHAR NOT NULL, supplier INTEGER REFERENCES Supplier(id), quantity INTEGER NOT NULL);")
    cursor.execute("CREATE TABLE suppliers(ID INTEGER PRIMARY KEY,name VARCHAR NOT NULL);")
    cursor.execute("CREATE TABLE orders(ID INTEGER PRIMARY KEY,location VARCHAR NOT NULL, hat INTEGER REFERENCES hats(id));")


def generate_orders(path):
    with open(path, 'r') as f:
        for line in f:
            yield line[:-1].split(',')


def execute_order(db_cursor, location, topping):
    first_command = f'SELECT hats.ID, hats.quantity, suppliers.name from hats JOIN suppliers ON hats.supplier=suppliers.ID WHERE hats.topping="{topping}" ORDER BY suppliers.ID'
    print(f'first command:\n{first_command}')
    db_cursor.execute(first_command)
    hat_id, current_topping_quantity, supplier = db_cursor.fetchone()
    if current_topping_quantity == 1:
        second_command = f'DELETE FROM hats WHERE ID = {hat_id}'
    else:
        second_command = f'UPDATE hats SET quantity = {int(current_topping_quantity) - 1} WHERE ID = {hat_id}'
    third_command = f'INSERT INTO orders VALUES(,?,?)'
    db_cursor.execute(third_command, (location, hat_id))
    # print(f'second_command:\n{second_command}')
    db_cursor.execute(second_command)
    return supplier


# cursor.execute("SELECT NAME FROM Students WHERE ID=(?)", (1,))
#     studentwithid1 = cursor.fetchone()
#     print("Student with id 1: " + str(studentwithid1))
#
#     # let's get the name of the student of id 5
#     cursor.execute("SELECT NAME FROM Students WHERE ID=(?)", (5,))
#     studentwithid5 = cursor.fetchone()
#     print("Student with id 5: " + str(studentwithid5))




if  __name__ == '__main__':
    config_path = sys.argv[1]
    orders_path = sys.argv[2]
    output_path = sys.argv[3]
    db_already_existed = os.path.isfile('myDB.db')
    db_con = sqlite3.connect('myDB.db')
    with db_con:
        cursor = db_con.cursor()
        if not db_already_existed:
            create_tables(cursor)
            populate_db_from_input(config_path, cursor)
        with open(output_path, 'w') as f:
            for location, topping in generate_orders(orders_path):
                supplier = execute_order(cursor, location, topping)
                f.write(','.join((topping, supplier, location)) + '\n')
# databaseexisted = os.path.isfile('example2.db')
#
# dbcon = sqlite3.connect('example2.db')
#
# with dbcon:
#     cursor = dbcon.cursor()
#     if not databaseexisted:  # First time creating the database. Create the tables
#         cursor.execute("CREATE TABLE Students(ID INTEGER PRIMARY KEY, NAME TEXT NOT NULL)")  # create table students
#         cursor.execute("INSERT INTO Students VALUES(?,?)",
#                        (1, 'Morad',))  # add entry 'id = 1, name = Morad' into the table.
#         cursor.execute("INSERT INTO Students VALUES(?,?)", (2, 'Harry Potter',))
#
#     # let's get all students and print their entries
#     cursor.execute("SELECT * FROM Students;")
#     studentslist = cursor.fetchall()
#     print("All students as list:")
#     print(studentslist)
#     print("All students one by one:")
#     for student in studentslist:
#         print("Student name: " + str(student))
#
#     # let's get the name of the student of id 1
#     cursor.execute("SELECT NAME FROM Students WHERE ID=(?)", (1,))
#     studentwithid1 = cursor.fetchone()
#     print("Student with id 1: " + str(studentwithid1))
#
#     # let's get the name of the student of id 5
#     cursor.execute("SELECT NAME FROM Students WHERE ID=(?)", (5,))
#     studentwithid5 = cursor.fetchone()
#     print("Student with id 5: " + str(studentwithid5))
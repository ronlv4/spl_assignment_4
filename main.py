import sqlite3

import os
import sys
from Repository import repo
from DTO.Hat import Hat
from DTO.Order import Order
from DTO.Supplier import Supplier


def populate_db_from_input(path):
    with open(path, 'r') as f:
        num_of_hats, num_of_suppliers = map(int, f.readline().split(','))
        for index, line in zip(range(num_of_hats), f):
            hat = Hat(*(line[:-1].split(',')))
            repo.hats.insert(hat)
        for index, line in zip(range(num_of_suppliers), f):
            supplier = Supplier(*(line[:-1].split(','))) if line[-1] == '\n' else Supplier(*(line.split(',')))
            repo.suppliers.insert(supplier)


def generate_orders(path):
    with open(path, 'r') as f:
        for line in f:
            yield line[:-1].split(',') if line[-1] == '\n' else line.split(',')


def execute_order(location, topping):
    hat_with_supplier = repo.get_hat_with_supplier(topping)
    if hat_with_supplier.hat_quantity == 1:
        repo.hats.delete(hat_with_supplier.hat_id)
    else:
        repo.hats.update_quantity(hat_with_supplier.hat_id, hat_with_supplier.hat_quantity - 1)
    repo.orders.insert(Order(location, hat_with_supplier.hat_id))
    return hat_with_supplier.supplier_name


def main():
    config_path, orders_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]
    if repo.create_tables():
        populate_db_from_input(config_path)
    with open(output_path, 'w') as f:
        for location, topping in generate_orders(orders_path):
            supplier = execute_order(location, topping)
            f.write(','.join((topping, supplier, location)) + '\n')


if __name__ == '__main__':
    main()

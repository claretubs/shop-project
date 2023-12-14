# OOP Shop - Shop Class
# Author: Clare Tubridy

import csv
from product import Product
from product_stock import ProductStock
from customer import Customer

class Shop:
    def __init__(self,path):
        # Initialize Shop with empty stock
        self.stock = []

        # Read shop data from the CSV file
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ",")
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            
            # Process each row in the CSV file to create stock items
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)

    def process_transaction(self, customer):
        # Calculate the total cost of the customer's order
        order_cost = customer.order_cost()

        if order_cost <= customer.budget:
            # Update shops cash and customers budget
            self.cash += order_cost
            customer.budget -= order_cost

            # Update stock quantities
            for shop_item in self.stock:
                for list_item in customer.shopping_list:
                    if list_item.name() == shop_item.name():
                        shop_item.quantity -= list_item.quantity

            print(f"Transaction succesful! {customer.name} paid €{order_cost}.")

        else:
            print(f"Transaction failed! {customer.name} cannot afford the order.")

    def __repr__(self):
        # Generate a string representation of the Shop object
        str = ""
        str += f"Shop has {self.cash} in cash \n"

        for item in self.stock:
            str += f"{item} \n"
        return str

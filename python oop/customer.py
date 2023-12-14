# OOP Shop - Customer Class
# Author: Clare Tubridy

import csv
from product import Product
from product_stock import ProductStock

class Customer:
    def __init__(self, path, shop_stock):
        self.shopping_list = []

        # Read customer data from CSV file
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ",")
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])

            # Process each row in the CSV file to create shopping list items
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])

                # Check if the product is stocked by the shop
                shop_item_names = [stock.name() for stock in shop_stock]
                if name not in shop_item_names:
                    print(f"Sorry, Product {name} is not in stock.")
                    continue
                
                # Create Product and ProductStock objects and add to the shopping list
                p = Product(name)
                ps = ProductStock(p, quantity)
                self.shopping_list.append(ps)
    
    def adjust_shopping_list(self, shop_stock):
        # Adjust shopping list quantities based on available stock
        for list_item in self.shopping_list:
            name = list_item.name()
            available_quantity = 0
            for stock in shop_stock:
                if stock.name() ==name:
                    available_quantity = stock.quantity
                    break

            if list_item.quantity > available_quantity:
                print(f"Warning: Not enough stock for {name}. Adjusting quantity to {available_quantity}.")
                list_item.quantity = available_quantity

    def calculate_costs(self, price_list):
        # Adjust shopping list and calculate total cost based on updated prices
        self.adjust_shopping_list(price_list)
        self.total_cost = 0

        for shop_item in price_list:
            for list_item in self.shopping_list:
                if (list_item.name() == shop_item.name()):
                    list_item.product.price = shop_item.unit_price()

    def order_cost(self):
        # Calculate the total cost of the shopping list
        cost = 0

        for list_item in self.shopping_list:
            cost += list_item.cost()
        return cost
    
    def __repr__(self):
        # Generate a representation of the customer and their shopping list
        str = f"{self.name} wants to buy:"
        for item in self.shopping_list:
            cost = round(item.cost(), 2)
            str += f"\n{item}"
            
            if (cost == 0):
                str += f". {self.name} doesnt know how much that costs : "
            else:
                str += f" COST: {cost}"

        str += f"\nThe cost would be: {self.order_cost()}, he would have {round(self.budget - self.order_cost(), 2)} left"
        return str
# Procedural Shop
# Author: Clare Tubridy

from dataclasses import dataclass, field
from typing import List
import csv

@dataclass
class Product:
    name: str
    price: float = 0.0

@dataclass 
class ProductStock:
    product: Product
    quantity: int

@dataclass
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)

def create_and_stock_shop():
     # Create and stock the shop with data from the CSV file
    s = Shop()
    with open('../stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
            #print(ps)
    return s

def calculate_costs(c, s):
    # Calculate costs for each item in the customer's shopping list
    for item in c.shopping_list:
        item.product.price = get_product_price(s, item.product.name)

def process_transaction(c, s):
    # Process a transaction for the customer in the shop
    total_cost = 0
    items_to_remove = []

    for item in c.shopping_list:
        product_price = get_product_price(s, item.product.name)
        if product_price is not None:
            cost = item.quantity * product_price
            total_cost += cost
            update_stock_quantities(s, item.product.name, item.quantity)
        else:
            print(f"Sorry, {item.product.name} is not in stock.")
            items_to_remove.append(item)

    # Remove items that are out of stock from the shopping list
    for item in items_to_remove:
        c.shopping_list.remove(item)
    
    # Check if the customer can afford the transaction
    if total_cost > 0 and total_cost <= c.budget:
        print(f"Transaction successful! {c.name} paid €{total_cost:.2f}.")
        c.budget -= total_cost
        s.cash += total_cost
    else:
        print(f"Transaction cancelled! Insufficient funds.")

def get_product_price(s, product_name):
    # Get the price of a product from the shop's stock
    for item in s.stock:
        if item.product.name == product_name:
            return item.product.price
    return None

def update_stock_quantities(s, product_name, requested_quantity):
    # Update stock quantities based on a customer's order
    for stock_item in s.stock:
        if stock_item.product.name == product_name:
            if requested_quantity <= stock_item.quantity:
                stock_item.quantity -= requested_quantity 
            else:
                print(f"\nSorry, there are only {stock_item.quantity} {product_name} in stock.")
                # Set the stock to zero if the requested quantity exceeds stock
                stock_item.quantity = 0
            break

def read_customer(file_path):
    # Read customer data from a CSV file
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        c = Customer(first_row[0], float(first_row[1]))
        for row in csv_reader:
            name = row[0]
            quantity = float(row[1])
            p = Product(name)
            ps = ProductStock(p, quantity)
            c.shopping_list.append(ps)
        return c 

def live_mode(s):
    # Simulate live shopping mode for the shop
    while True:
        print("\nLive Mode - Enter 'exit' to end the session.")

        # Get product name from the user
        product_name = input("Enter product name: ")

         # Check if the user wants to exit
        if product_name.lower() == 'exit':
            break

        # Get quantity from the user
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity. Please enter a valid number.")
            continue

        # Check if the product is in stock
        product_price = get_product_price(s, product_name)
        if product_price is not None:
            cost = quantity * product_price
            print(f'The cost for {quantity} {product_name}(s) will be €{cost:.2f}')

            # Process the transaction
            if cost > 0 and cost <= s.cash:
                print(f"Transaction successful! Shop received €{cost:.2f}.")
                s.cash += cost
                update_stock_quantities(s, product_name, quantity)
            else:
                print("Transaction cancelled! Insufficient funds.")
        else:
            print(f"Sorry, {product_name} is not in stock.")

    print("Exiting live mode.")

def print_product(p):
    # Print details of a product
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: {p.price}')

def print_customer(c, s):
    # Print details of a customer and their shopping list
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    for item in c.shopping_list:
        print_product(item.product)
        
        product_price = get_product_price(s, item.product.name)
        if product_price is not None:
            print(f'{c.name} ORDERS {item.quantity} OF ABOVE PRODUCT')
            cost = item.quantity * item.product.price
            print(f'The cost to {c.name} will be €{cost:.2f}')
        else:
            print(f"Sorry, {item.product.name} is not in stock.")
        
def print_shop(s):
    # Print details of the shop, including cash and stock
    print(f'\nShop has {s.cash:.2f} in cash')
    for item in s.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')


# Example usage
s = create_and_stock_shop()
#c = read_customer("../customer.csv")
#c = read_customer("../customer_no_stock.csv")
c = read_customer("../customer_cant_afford.csv")
#calculate_costs(c,s)
#print_customer(c,s)
#process_transaction(c,s)
live_mode(s)
print_shop(s)
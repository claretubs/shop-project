# OOP Shop - Product Class
# Author: Clare Tubridy

class Product:
    def __init__(self, name, price=0):
        # Initialize Product with a name and price
        self.name = name
        self.price = price

    def __repr__(self):
         # Generate a string representation of the Product object
        return f"NAME: {self.name} | PRICE: {self.price} |"
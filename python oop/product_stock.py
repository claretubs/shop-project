# OOP Shop - ProductStock Class
# Author: Clare Tubridy

class ProductStock:
    def __init__(self, product, quantity):
        # Initialize ProductStock with a product and quantity
        self.product = product
        self.quantity = quantity

    def name(self):
        # Get the name of the product in the stock
        return self.product.name
    
    def unit_price(self):
        # Get the unit price of the product in the stock
        return self.product.price
    
    def cost(self):
        # Calculate the total cost of the product in the stock
        return self.unit_price() * self.quantity

    def __repr__(self):
        # Generate a string representation of the ProductStock object
        return f"{self.product} QUANTITY: {self.quantity}"
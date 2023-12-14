# OOP Shop - Live mode
# Author: Clare Tubridy

from shop import Shop
from customer import Customer
from product import Product
from product_stock import ProductStock

def main():
    # Load shop and customer data
    s = Shop("../stock.csv")
    c = Customer("../customer.csv", s.stock)
    #c = Customer("../customer_no_stock.csv", s.stock)
    #c = Customer("../customer_cant_afford.csv", s.stock)

    # Display initial state
    print("Initial Shop State:")
    print(s)

    # Continuous loop for live shopping mode
    while True:
        print("\nCustomer's Updated Shopping List:")
        print(c)

        # Get product name from user input (or 'exit' to finish)
        product_name = input("\nEnter product name (or 'exit' to finish): ").strip()

        if product_name == "exit":
            break

        # Check if the product is stocked by the shop
        shop_item_names =[stock.name() for stock in s.stock]
        if product_name not in shop_item_names:
            print(f"Sorry, {product_name} is not in stock.")
            continue

        quantity = int(input(f"Enter the quantity for {product_name}: "))

        # Add product to the customer's shopping list and calculate costs
        c.shopping_list.append(ProductStock(Product(product_name), quantity))
        c.calculate_costs(s.stock)

        # Process the transaction in the shop
        s.process_transaction(c)

    print("\nFinal Shop State:")
    print(s)

if __name__ == "__main__":
    main()
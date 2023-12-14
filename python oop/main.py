# OOP Shop - Main
# Author: Clare Tubridy

from shop import Shop
from customer import Customer

def main():
    # Load shop and customer data
    s = Shop("../stock.csv")
    #c = Customer("../customer.csv", s.stock)
    #c = Customer("../customer_no_stock.csv", s.stock)
    c = Customer("../customer_cant_afford.csv", s.stock)

    # Display initial state
    print("Initial Shop State:")
    print(s)

    # Calculate costs and update prices in the customer's shopping list
    c.calculate_costs(s.stock)

    print("\nCustomer's Updated Shopping List:")
    print(c)

    s.process_transaction(c)

    print("\nFinal Shop State:")
    print(s)

    # Check if the customer can afford the order
    if c.order_cost() <= c.budget:
        print("\nTransaction Successful! Thank you for shopping.")
    else:
        print("\nTransaction Failed! The customer cannot afford the order.")

if __name__ == "__main__":
    main()
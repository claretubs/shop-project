// Shop using Structures in C
// Author: Clare Tubridy

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct Product {
	char* name;
	double price;
};

struct ProductStock {
	struct Product product;
	int quantity;
};

struct Shop {
	double cash;
	struct ProductStock stock[20];
	int index;
};

struct Customer {
	char* name;
	double budget;
	struct ProductStock shoppingList[10];
	int index;
};

// Function to print product details
void printProduct(struct Product p)
{
	printf("PRODUCT NAME: %s \nPRODUCT PRICE: %.2f\n", p.name, p.price);
	printf("-------------\n");
}

// Function to print customer details and shopping list
void printCustomer(struct Customer c)
{
	printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: %.2f\n", c.name, c.budget);
	printf("-------------\n");
	for(int i = 0; i < c.index; i++)
	{
		printProduct(c.shoppingList[i].product);
		printf("%s ORDERS %d OF ABOVE PRODUCT\n", c.name, c.shoppingList[i].quantity);
		double cost = c.shoppingList[i].quantity * c.shoppingList[i].product.price; 
		printf("The cost to %s will be €%.2f\n\n", c.name, cost);
	}
}

// Function to create and stock the shop with data from a CSV file
struct Shop createAndStockShop(char* filePath)
{
    FILE* fp;
    char line[256];  
    float cash;

    fp = fopen(filePath, "r");
    if (fp == NULL) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    // Read the first line to get the cash value
    if (fgets(line, sizeof(line), fp) != NULL) {
        cash = atof(line);
        struct Shop s = {cash};

        // Read the remaining lines to get stock information
        while (fgets(line, sizeof(line), fp) != NULL) {
            char *n = strtok(line, ",");
            char *p = strtok(NULL, ",");
            char *q = strtok(NULL, ",");
            int quantity = atoi(q);
            double price = atof(p);
            char *name = malloc(sizeof(char) * 50);
            strcpy(name, n);
            struct Product product = {name, price};
            struct ProductStock stockItem = {product, quantity};
            s.stock[s.index++] = stockItem;
        }

        fclose(fp);
        return s;
    } else {
        fclose(fp);
        perror("Error reading file");
        exit(EXIT_FAILURE);
    }
}

// Function to read customer orders
struct Customer readCustomerOrders(char* filePath) 
{
    FILE* fp;
    char line[256];  
    double budget;

    fp = fopen(filePath, "r");
    if (fp == NULL) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    // Read the first line to get the customer details
    if (fgets(line, sizeof(line), fp) != NULL) {
        char *n = strtok(line, ",");
        char *b = strtok(NULL, ",");
        budget = atof(b);

        // Allocating memory for the name
        char *name = malloc(strlen(n) + 1);
        strcpy(name, n);

        // Creating the customer struct
        struct Customer c = {name, budget};

        // Read the remaining lines to get the shopping list
        while (fgets(line, sizeof(line), fp) != NULL) {
            char *p = strtok(line, ",");
            char *q = strtok(NULL, ",");
            int quantity = atoi(q);
            char *pname = malloc(sizeof(char) * 50);
            strcpy(pname, p);
            struct Product product = {pname};
            struct ProductStock stockItem = {product, quantity};
            c.shoppingList[c.index++] = stockItem;
        }

        fclose(fp);
        return c;
    } else {
        fclose(fp);
        perror("Error reading file");
        exit(EXIT_FAILURE);
    }
}

// Function to process a transaction
void processTransaction(struct Customer* c, struct Shop* s) {
    double totalCost = 0;
    // Flag to check if any item is in stock
    int itemsInStock = 0; 

    for (int i = 0; i < c->index; i++) {
        int productInStock = 0;

        for (int j = 0; j < s->index; j++) {
            if (strcmp(c->shoppingList[i].product.name, s->stock[j].product.name) == 0) {
                double cost = 0;

                if (c->shoppingList[i].quantity > s->stock[j].quantity) {
                    // Customer ordered more than what is in stock
                    printf("Warning: There are only %d %s in stock. Charging for available quantity.\n", s->stock[j].quantity, c->shoppingList[i].product.name);
                    cost = s->stock[j].quantity * s->stock[j].product.price;
                    // Set stock to 0
                    s->stock[j].quantity = 0; 
                } else {
                    cost = c->shoppingList[i].quantity * s->stock[j].product.price;
                    s->stock[j].quantity -= c->shoppingList[i].quantity;
                }

                totalCost += cost;
                productInStock = 1;
                itemsInStock = 1;
                break;
            }
        }

        if (!productInStock) {
            // Product not found in stock
            printf("Sorry, %s is not in stock. Removing it from the order.\n", c->shoppingList[i].product.name);
            // Remove the item from the order
            c->shoppingList[i] = c->shoppingList[--c->index]; 
            // Recheck the current index as it's replaced with the last item
            i--; 
        }
    }

    if (itemsInStock) {
        if (totalCost > 0 && totalCost <= c->budget) {
            printf("Transaction successful! Customer paid €%.2f.\n", totalCost);
            c->budget -= totalCost;
            s->cash += totalCost;
        } else {
            printf("Transaction cancelled! Insufficient funds.\n");
        }
    } else {
        printf("Transaction cancelled! No items in stock.\n");
    }
}

// Function to print shop details
void printShop(struct Shop s)
{
	printf("Shop has %.2f in cash\n", s.cash);
	for (int i = 0; i < s.index; i++)
	{
		printProduct(s.stock[i].product);
		printf("The shop has %d of the above\n\n", s.stock[i].quantity);
	}
}

// Function for live mode
void liveMode(struct Shop* s) {
    char product_name[50];
    int quantity;

    while (1) {
        printf("\nLive Mode - Enter 'exit' to end the session.\n");

        printf("Enter product name: ");
        scanf("%s", product_name);

        // Check if the user wants to exit
        if (strcmp(product_name, "exit") == 0) {
            break;
        }

        printf("Enter quantity: ");
        scanf("%d", &quantity);

        // Check if the product is in stock
        int found = 0;
        for (int i = 0; i < s->index; i++) {
            if (strcmp(product_name, s->stock[i].product.name) == 0) {
                found = 1;
                double cost = quantity * s->stock[i].product.price;
                printf("The cost for %d %s(s) will be €%.2f\n", quantity, product_name, cost);

                // Process the transaction
                if (cost > 0 && cost <= s->cash && quantity <= s->stock[i].quantity) {
                    printf("Transaction successful! Shop received €%.2f.\n", cost);
                    s->cash += cost;
                    s->stock[i].quantity -= quantity;
                } else {
                    printf("Transaction cancelled! Insufficient funds or out of stock.\n");
                }
                break;
            }
        }

        if (!found) {
            printf("Sorry, %s is not in stock.\n", product_name);
        }
    }

    printf("Exiting live mode.\n");
}

int main(void) 
{
	struct Shop s = createAndStockShop("../stock.csv");
    struct Customer c = readCustomerOrders("../customer.csv");
    //struct Customer c = readCustomerOrders("../customer_no_stock.csv");
	//struct Customer c = readCustomerOrders("../customer_cant_afford.csv");

	printShop(s);
	printCustomer(c);

    processTransaction(&c, &s);

    printShop(s);

    liveMode(&s);

    printShop(s);

    return 0;
}
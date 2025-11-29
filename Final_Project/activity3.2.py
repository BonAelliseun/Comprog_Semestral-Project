INVENTORY = {"CEMENT":{"QUANTITY":100,"PRICE":459},
    "BRICKS":{"QUANTITY":100,"PRICE":459},
    "BRICKS":{"QUANTITY":100,"PRICE":459},
    'SAND':{"QUANTITY": 2000, "PRICE": 100},
    'STEEL':{"QUANTITY": 2000, "PRICE": 100},
    'CONCREET':{"QUANTITY":2000, "PRICE": 100}}

print("THE INVENTORY")

for name, values in INVENTORY.items():
    print("item name:",name,"QUANTITY:",values["QUANTITY"],"PRICE:",values["PRICE"])

print("\nOPERATIONS")
print("1.ADD ITEMS TO INVENTORY")
print("2.DELETE ITEMS TO INVENTORY")
print("3.EDIT ITEMS PRICE OR QUANTITY")
print("4.VIEW INVENTORY")
print("5.EXIT PROGRAM")

user_option = int(input("ENTER CHOICE (1-5): "))
print()

def add_item():
    print("ADD ITEMS TO INVENTORY")
    item_name = input("Enter Item Name: ").upper()
    if item_name not in INVENTORY:
        quanity = int(input("Enter Quantity of the item: "))
        price = float(input("Enter the price of the item: "))
        INVENTORY[item_name]={"QUANTITY":quanity,"PRICE":price}
        print()
        print(f" ----{item_name} has been added to Inventory---- ")
        view_inventory()
    else:
        print("The item you want to add is already part of the Inventory")

def delete_item():
    print("DELETE ITEMS TO INVENTORY")
    delete_item = input("Enter Item name you want to delete: ").upper()
    if delete_item in INVENTORY:
        del INVENTORY[delete_item]
        print()
        print(f" ----{delete_item} has been deleted to Inventory---- ")
        view_inventory()
    else:
        print("The item you want to delete is not part of the Inventory")

def edit_inventory():
    print("EDIT ITEMS PRICE OR QUANTITY IN INVENTORY")
    ask = int(input("Choose what do you want to edit (1.QUANTITY 2.PRICE 3.Both): "))
    if ask == 1:
        edit_name = input("Enter Item name you want to edit: ").upper()
        if edit_name in INVENTORY:
                print("Edit the Quantity")
                new_quantity = int(input("Enter new Quantity of the item: "))
                INVENTORY[edit_name]["QUANTITY"]=new_quantity
                print()
                print(f" ----{edit_name} quantity successfully edited----")
                view_inventory()
        else:
            print("Item does not exist")
    elif ask == 2:
        edit_name = input("Enter Item name you want to edit: ").upper()
        if edit_name in INVENTORY:
            print("Edit the Price")
            new_price = int(input("Enter new PRICE of the item: "))
            INVENTORY[edit_name]["PRICE"]=new_price
            print()
            print(f" ----{edit_name} price successfully edited---- ")
            view_inventory()
        else:
            print("Item does not exist")
    elif ask == 3:
        edit_name = input("Enter Item name you want to edit: ").upper()
        if edit_name in INVENTORY:
            print("Edit both Price and quantity")
            new_price = int(input("Enter new PRICE of the item: "))
            new_quantity = int(input("Enter new Quantity of the item: "))
            INVENTORY[edit_name]["PRICE"]=new_price
            INVENTORY[edit_name]["QUANTITY"]=new_quantity
            print()
            print(f" ----{edit_name} price and quantity successfully edited---- ")
            view_inventory()
        else:
            print("Item does not exist")
    else:
        print("Select between 1-3 only")

def view_inventory():
    if len(INVENTORY) == 0:
        print("THE INVENTORY IS EMPTY")
    else:
        print("="*50)
        print()
        
        for name, values in INVENTORY.items():
            print("item name:",name,"QUANTITY:",values["QUANTITY"],"PRICE:",values["PRICE"])

        print()
        print("="*50)
        
if user_option == 1:
    add_item()
elif user_option == 2:
    delete_item()
elif user_option == 3:
    edit_inventory()
elif user_option == 4:
    view_inventory()
elif user_option == 5:
    print("EXIT PROGRAM")
else:
    print("SELECT BETWEEN 1-5 ONLY")
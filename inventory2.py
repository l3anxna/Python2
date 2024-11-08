class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.borrowed_items = {}

    def borrow_item(self, item_name: str, quantity: int) -> None:
        """Add an item to the user's borrowed items."""
        if item_name in self.borrowed_items:
            self.borrowed_items[item_name] += quantity
        else:
            self.borrowed_items[item_name] = quantity

    def return_item(self, item_name: str, quantity: int) -> bool:
        """Return an item from the user's borrowed items."""
        if item_name in self.borrowed_items:
            if self.borrowed_items[item_name] >= quantity:
                self.borrowed_items[item_name] -= quantity
                if self.borrowed_items[item_name] == 0:
                    del self.borrowed_items[item_name]
                return True
        return False

    def __str__(self) -> str:
        """String representation of the user."""
        return f"User: {self.name}, Borrowed Items: {self.borrowed_items}"

class InventorySystem:
    def __init__(self) -> None:
        self.inventory = {}
        self.users = {}
        self.load_inventory()
        self.load_transactions()

    def load_inventory(self) -> None:
        """Load inventory from a text file."""
        try:
            with open("inventory.txt", "r") as file:
                for line in file:
                    item_name, quantity = line.strip().split(": ")
                    self.inventory[item_name] = int(quantity)
            print("Inventory loaded successfully.")
        except FileNotFoundError:
            print("No inventory file found. Starting with an empty inventory.")
        except ValueError as e:
            print(f"Error loading inventory data: {e}. Starting with an empty inventory.")

    def save_inventory(self) -> None:
        """Save inventory to a text file."""
        with open("inventory.txt", "w") as file:
            for item_name, quantity in self.inventory.items():
                file.write(f"{item_name}: {quantity}\n")
        print("Inventory saved successfully.")

    def log_transaction(self, action: str, borrower_name: str, 
                        item_name: str, quantity: int) -> None:
        """Log lending transactions."""
        with open("transaction_log.txt", "a") as log_file:
            log_file.write(f"{action} | {borrower_name} | {item_name} | {quantity}\n")

    def load_transactions(self) -> None:
        """Load transactions from the log file without modifying inventory."""
        try:
            with open("transaction_log.txt", "r") as log_file:
                for line in log_file:
                    action, borrower_name, item_name, quantity = line.strip().split(" | ")
                    quantity = int(quantity)
                    if borrower_name not in self.users:
                        self.users[borrower_name] = User(borrower_name)
                    if action == "Lend":
                        self.users[borrower_name].borrow_item(item_name, quantity)
            print("Transactions loaded successfully.")
        except FileNotFoundError:
            print("No transaction log file found. Starting with an empty transaction history.")
        except ValueError as e:
            print(f"Error loading transaction data: {e}.")

    def is_valid_item_name(self, item_name: str) -> bool:
        """Check if the item name is valid (more than 2 characters and contains only letters)."""
        assert isinstance(item_name, str), "Item name must be a string."
        return item_name.isalpha() and len(item_name) > 2

    def add_item(self) -> None:
        """Add an item to the inventory."""
        item_name = input("Enter the item name: ").strip().lower()
        while not self.is_valid_item_name(item_name):
            print("Invalid item name! Please enter a name with at least 3 characters and without numbers or special characters.")
            item_name = input("Enter the item name: ").strip().lower()
        
        while True:
            try:
                item_quantity = int(input("Enter the item quantity: "))
                assert item_quantity > 0, "Quantity must be a positive integer."
                if item_name in self.inventory:
                    self.inventory[item_name] += item_quantity
                else:
                    self.inventory[item_name] = item_quantity
                print(f"\nAdded {item_quantity} of {item_name} to the inventory.")
                # Save inventory after adding an item
                self.save_inventory()
                break
            except ValueError:
                print("Please enter a valid integer for quantity.")
            except AssertionError as e:
                print(e)

    def view_inventory(self):
        """View the current inventory in different formats."""
        print("\nChoose how you want to view the inventory:")
        print("1. View as a simple list")
        print("2. View in alphabetical order")
        print("3. View sorted by quantity")
        
        choice = input("Select an option (1-3): ")
        
        if choice == '1':
            print("\n===============================")
            print(" Current Inventory ")
            print("===============================")
            if not self.inventory:
                print("The inventory is empty.")
            else:
                for index, (item, quantity) in enumerate(self.inventory.items(), start=1):
                    print(f"{index}. {item}: {quantity}")
            print("===============================")
        
        elif choice == '2':
            print("\n===============================")
            print(" Items in Alphabetical Order ")
            print("===============================")
            if not self.inventory:
                print("The inventory is empty.")
            else:
                for index, item in enumerate(sorted(self.inventory.keys(), key=lambda x: x.lower()), start=1):
                    print(f"{index}. {item}: {self.inventory[item]}")
            print("===============================")
        
        elif choice == '3':
            print("\n===============================")
            print(" Items Sorted by Quantity ")
            print("===============================")
            if not self.inventory:
                print("The inventory is empty.")
            else:
                for index, (item, quantity) in enumerate(sorted(self.inventory.items(), 
                    key=lambda x: x[1], reverse=True), start=1):
                    print(f"{index}. {item}: {quantity}")
            print("===============================")
        
        else:
            print("Invalid choice! Please select 1, 2, or 3.")

    def lend_item(self) -> None:
        """Lend an item from the inventory."""
        borrower_name = input("Enter your name: ").strip()
        if borrower_name not in self.users:
            self.users[borrower_name] = User(borrower_name)

        available_items = {key.lower(): value for key, value in self.inventory.items() if value > 0}
        if not available_items:
            print("No items available for lending.")
            return

        print("\nAvailable items for lending:")
        for index, (item_name, quantity) in enumerate(available_items.items()):
            print(f"{index + 1}. {item_name}: {quantity}")

        try:
            item_index = int(input("Select the item number you want to lend: ")) - 1
            if item_index < 0 or item_index >= len(available_items):
                print("Invalid selection. Please try again.")
                return
            
            chosen_item = list(available_items.keys())[item_index]
            available_quantity = available_items[chosen_item]
            lend_quantity = int(input(f"How many of {chosen_item} do you want to lend? "))
            
            if lend_quantity <= 0 or lend_quantity > available_quantity:
                print("Invalid quantity selected.")
                return

            self.users[borrower_name].borrow_item(chosen_item, lend_quantity)
            self.inventory[chosen_item] -= lend_quantity
            print(f"Lent {lend_quantity} of {chosen_item} to {borrower_name}.")

            self.log_transaction("Lend", borrower_name, chosen_item, lend_quantity)

            self.save_inventory()

        except ValueError:
            print("Please enter a valid integer.")

    def return_item(self) -> None:
        """Return a lent item back to the inventory."""
        borrower_name = input("Enter your name: ").strip()
        
        if borrower_name not in self.users or not self.users[borrower_name].borrowed_items:
            print(f"No records found for {borrower_name}.")
            return
        
        user = self.users[borrower_name]
        
        if user.borrowed_items:
            print("\nItems you have borrowed:")
            
            for index, (item_name, quantity) in enumerate(user.borrowed_items.items(), start=1):
                print(f"{index}. {item_name}: {quantity}")
            
            try:
                item_index = int(input("Select the number of the item you want to return: ")) - 1
                
                if item_index < 0 or item_index >= len(user.borrowed_items):
                    print("Invalid selection. Please try again.")
                    return
                
                chosen_item = list(user.borrowed_items.keys())[item_index]
                
                return_quantity = int(input(f"How many of {chosen_item} do you want to return? "))
                
                if user.return_item(chosen_item, return_quantity):
                    self.inventory[chosen_item] += return_quantity
                    print(f"Returned {return_quantity} of {chosen_item} from {borrower_name}.")
                    
                    self.log_transaction("Return", borrower_name, chosen_item, return_quantity)
                    
                    self.save_inventory()
                
                else:
                    print(f"You do not have enough of {chosen_item} to return.")
            
            except ValueError:
                print("Please enter a valid integer.")

    def view_lending_records(self) -> None:
        """View all current lending records."""
        
        if not self.users or all(not user.borrowed_items for user in self.users.values()):
            print("\nNo current lending records.")
        
        for user in self.users.values():
            if user.borrowed_items:
                items_list = ', '.join([f"{key}: {value}" for key, value in user.borrowed_items.items()])
                print(f"{user.name}: {items_list}")

    def update_item(self) -> None:
        """Update the quantity of an existing item."""
        item_name = input("Enter the item name to update: ")
        
        while not self.is_valid_item_name(item_name):
            print("Invalid item name! Please enter a name without numbers or special characters.")
            item_name = input("Enter the item name to update: ")
        
        if item_name in self.inventory:
            
            try:
                new_quantity = int(input(f"Enter new quantity for {item_name}: "))
                
                assert new_quantity >= 0, "Quantity must be a non-negative integer."
                
                old_quantity = self.inventory[item_name]
                
                self.inventory[item_name] = new_quantity
                
                print(f"Updated {item_name} from {old_quantity} to {new_quantity}.")
                
                self.save_inventory()
            
            except ValueError:
                print("Please enter a valid integer for quantity.")
            
            except AssertionError as e:
                print(e)

    def bulk_add_items(self) -> None:
        """Add multiple items to the inventory at once."""
        while True:
            item_name = input("Enter the item name (or type 'done' to finish): ").strip().lower()
            if item_name == "done":
                break
            
            while not self.is_valid_item_name(item_name):
                print("Invalid Item Name! Please enter a name without numbers or special characters.")
                item_name = input("Enter The Item Name (or Type 'done' To Finish): ").strip().lower()
                if item_name == "done":
                    return
            
            try:
                item_quantity = int(input("Enter The Quantity: "))
                assert item_quantity > 0, "Quantity Must Be A Positive Integer."
                
                if item_name in self.inventory:
                    old_quantity = self.inventory[item_name]
                    new_quantity = old_quantity + item_quantity
                    self.inventory[item_name] += item_quantity
                    print(f"Added {item_quantity} of {item_name}. New Total Is Now {new_quantity}.")
                else:
                    self.inventory[item_name] = item_quantity
                    print(f"Added New Item '{item_name}' With Quantity Of {item_quantity}.")
                
                self.save_inventory()
                
            except ValueError:
                print("Please Enter A Valid Integer For Quantity.")
            except AssertionError as e:
                print(e)

    def main_menu(self) -> None:
        """Display The Main Menu And Handle User Choices."""
        while True:
            options = [
                "1. Add Item",
                "2. View Inventory",
                "3. Lend Item",
                "4. Return Item",
                "5. View Lending Records",
                "6. Update Item Quantity",
                "7. Bulk Add Items",
                "8. Exit"
            ]
            for option in options:
                print(option)
            
            choice = input("\nChoose An Option (1-8): ")
            
            if choice == '1':
                self.add_item()
            elif choice == '2':
                self.view_inventory()
            elif choice == '3':
                self.lend_item()
            elif choice == '4':
                self.return_item()
            elif choice == '5':
                self.view_lending_records()
            elif choice == '6':
                self.update_item()
            elif choice == '7':
                self.bulk_add_items()
            elif choice == '8':
                print("\nExiting The Inventory System.")  # Save Before Exiting.
                self.save_inventory()
                break
            else:
                print("\nInvalid Choice! Please Choose A Valid Option.")

if __name__ == "__main__":
    system = InventorySystem()
    system.main_menu()

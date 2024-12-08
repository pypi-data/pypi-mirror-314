import argparse
import json
import os

# File where the expenses will be stored
EXPENSES_FILE = "expenses.json"

def load_expenses():
    """
    Load expenses from the file.

    Returns:
        list: A list of expenses loaded from the JSON file. If the file doesn't exist,
              an empty list is returned.
    """
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    """
    Save the expenses list to the file.

    Args:
        expenses (list): The list of expenses to be saved in the file.
    """
    with open(EXPENSES_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense(category, amount, description):
    """
    Add an expense interactively or via command-line arguments.

    Args:
        category (str): The category of the expense.
        amount (float): The amount of the expense.
        description (str): A description of the expense.
    """
    expenses = load_expenses()
    expense_id = len(expenses) + 1  # Simple auto-incrementing ID
    expense = {"id": expense_id, "category": category, "amount": amount, "description": description}
    
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added: {category}, {amount}, {description}")

def remove_expense(expense_id):
    """
    Remove an expense by its ID.

    Args:
        expense_id (int): The ID of the expense to remove.
    """
    expenses = load_expenses()
    expense = next((exp for exp in expenses if exp['id'] == expense_id), None)
    
    if expense:
        expenses.remove(expense)
        save_expenses(expenses)
        print(f"Expense with ID {expense_id} removed.")
    else:
        print(f"Expense with ID {expense_id} not found.")

def list_expenses():
    """
    List all expenses interactively.

    Prints all expenses stored in the expenses file. If no expenses exist, 
    prints a message indicating that no expenses are found.
    """
    expenses = load_expenses()
    if expenses:
        print("List of Expenses:")
        for expense in expenses:
            print(f"ID: {expense['id']} | Category: {expense['category']} | Amount: {expense['amount']} | Description: {expense['description']}")
    else:
        print("No expenses found.")

def interactive_mode():
    """
    Run the program in interactive mode to handle user input for commands.

    This function allows the user to add, remove, or list expenses interactively.
    The user can also exit the program from this mode.
    """
    while True:
        print("\n--- Budget Tracker ---")
        print("1. Add Expense")
        print("2. Remove Expense")
        print("3. List Expenses")
        print("4. Exit")
        
        choice = input("Please choose an option (1-4): ")
        
        if choice == "1":
            category = input("Enter the category of the expense: ")
            amount = float(input("Enter the amount of the expense: "))
            description = input("Enter a description for the expense: ")
            add_expense(category, amount, description)
        elif choice == "2":
            expense_id = int(input("Enter the ID of the expense to remove: "))
            remove_expense(expense_id)
        elif choice == "3":
            list_expenses()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

def main():
    """
    Main function to handle command-line arguments and user input.

    This function parses command-line arguments and calls the appropriate function 
    to add, remove, or list expenses, or run the program in interactive mode.
    """
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Budget Tracker Command Line Tool")
    
    parser.add_argument('--add', nargs=3, metavar=('CATEGORY', 'AMOUNT', 'DESCRIPTION'), help="Add an expense")
    parser.add_argument('--remove', metavar='ID', type=int, help="Remove an expense by ID")
    parser.add_argument('--list', action='store_true', help="List all expenses")
    parser.add_argument('--interactive', action='store_true', help="Run the program in interactive mode")

    # Parse the arguments
    args = parser.parse_args()

    # Handle command-line options
    if args.add:
        category, amount, description = args.add
        try:
            amount = float(amount)
            add_expense(category, amount, description)
        except ValueError:
            print("Invalid amount. Please enter a valid number for the amount.")
    elif args.remove:
        remove_expense(args.remove)
    elif args.list:
        list_expenses()
    elif args.interactive:
        interactive_mode()
    else:
        print("No valid command provided. Use --help for usage instructions.")

if __name__ == "__main__":
    main()
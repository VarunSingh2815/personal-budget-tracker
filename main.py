import json
import os
import tkinter as tk
from tkinter import messagebox

# Define the filename for storing transactions
data_file = "transactions.json"

# Initialize the transaction list
transactions = []

# Check if the data file exists and load transactions
if os.path.exists(data_file):
    with open(data_file, "r") as file:
        transactions = json.load(file)


def save_transactions():
    # Save transactions to the data file
    with open(data_file, "w") as file:
        json.dump(transactions, file)


def add_transaction():
    transaction_type = type_var.get().capitalize()
    transaction_category = category_entry.get()
    try:
        transaction_amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")
        return

    transactions.append({"type": transaction_type, "category": transaction_category, "amount": transaction_amount})
    save_transactions()
    messagebox.showinfo("Success", "Transaction added successfully!")
    clear_entry_fields()


def calculate_budget():
    income = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "Income")
    expenses = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "Expense")
    return income - expenses


def expense_analysis():
    expense_categories = set(
        transaction["category"] for transaction in transactions if transaction["type"] == "Expense")

    analysis_window = tk.Toplevel(root)
    analysis_window.title("Expense Analysis")

    for category in expense_categories:
        category_total = sum(transaction["amount"] for transaction in transactions if
                             transaction["type"] == "Expense" and transaction["category"] == category)
        label = tk.Label(analysis_window, text=f"{category}: ${category_total:.2f}")
        label.pack()


def clear_entry_fields():
    type_var.set("")  # Clear the transaction type
    category_entry.delete(0, tk.END)  # Clear the category entry field
    amount_entry.delete(0, tk.END)  # Clear the amount entry field


# Create the main application window
root = tk.Tk()
root.title("PERSONAL BUDGET TRACKER")

# Create a frame to organize the income and expense trackers
frame = tk.Frame(root)
frame.pack()

# Transaction Type Label and Radiobuttons
type_var = tk.StringVar()
type_label = tk.Label(frame, text="Transaction type:")
type_label.grid(row=0, column=0)
income_radio = tk.Radiobutton(frame, text="Income", variable=type_var, value="Income")
expense_radio = tk.Radiobutton(frame, text="Expense", variable=type_var, value="Expense")
income_radio.grid(row=0, column=1)
expense_radio.grid(row=0, column=2)

# Transaction Category Label and Entry Field
category_label = tk.Label(frame, text="Transaction category:")
category_label.grid(row=1, column=0)
category_entry = tk.Entry(frame)
category_entry.grid(row=1, column=1)

# Transaction Amount Label and Entry Field
amount_label = tk.Label(frame, text="Transaction amount:")
amount_label.grid(row=2, column=0)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=2, column=1)

# Add Income/Expense Transaction Button
add_button = tk.Button(frame, text="Add Transaction", command=add_transaction)
add_button.grid(row=3, column=0, columnspan=1)

# Calculate Budget Button
budget_button = tk.Button(frame, text="Calculate Budget",
                          command=lambda: messagebox.showinfo("Budget", f"Remaining Budget: ${calculate_budget():.2f}"))
budget_button.grid(row=3, column=1, columnspan=1)

# Expense Analysis Button
analysis_button = tk.Button(frame, text="Expense Analysis", command=expense_analysis)
analysis_button.grid(row=3, column=2, columnspan=1)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

# Start the Tkinter main loop
root.mainloop()

# Print "Goodbye!" after the Tkinter main loop exits
print("Goodbye!")

import tkinter as tk
from tkinter import ttk

# Function to dynamically create input fields for yearly installments based on the lease term
def create_yearly_installments():
    try:
        # Clear any existing entries
        for widget in yearly_frame.winfo_children():
            widget.destroy()

        # Get the lease term entered by the user
        lease_term = int(entry_lease_term.get())

        # Create labels and entries for each year's installment dynamically
        yearly_installments.clear()
        for year in range(1, lease_term + 1):
            tk.Label(yearly_frame, text=f"Year {year} Installment (R):", bg="#f0f0f0").grid(row=year-1, column=0, pady=5)
            entry = tk.Entry(yearly_frame, width=30)
            entry.grid(row=year-1, column=1, pady=5)
            yearly_installments.append(entry)

    except ValueError:
        # Handle invalid input for lease term
        error_label.config(text="Please enter a valid number of years.")

# Function to calculate Operating Lease details: Lease Expense, Accrued Expense, Prepaid Expense
def calculate_operating_lease():
    try:
        lease_term = int(entry_lease_term.get())
        total_installment = 0
        yearly_costs = []

        # Collect the total of all yearly payments
        for entry in yearly_installments:
            installment = float(entry.get())
            total_installment += installment

        # Calculate the straight-line lease expense (this is the value to be used in the income statement)
        straight_line_lease_expense = total_installment / lease_term

        # Calculate Accrued and Prepaid Expenses for each year
        total_accrued_expense = 0
        total_prepaid_expense = 0

        yearly_costs.append(f"Straight-line Lease Expense per Year: R{straight_line_lease_expense:.2f}")

        for year, entry in enumerate(yearly_installments, start=1):
            actual_payment = float(entry.get())
            difference = actual_payment - straight_line_lease_expense

            if difference > 0:
                total_prepaid_expense += difference
                yearly_costs.append(f"Year {year}: Prepaid Expense: R{difference:.2f}")
            elif difference < 0:
                total_accrued_expense += abs(difference)
                yearly_costs.append(f"Year {year}: Accrued Expense: R{abs(difference):.2f}")
            else:
                yearly_costs.append(f"Year {year}: No Accrued or Prepaid Expense")

        # Display the total accrued and prepaid expenses
        lease_expense_label.config(text=f"Total Lease Expense: R{total_installment:.2f}")
        accrued_expense_label.config(text=f"Total Accrued Expense: R{total_accrued_expense:.2f}")
        prepaid_expense_label.config(text=f"Total Prepaid Expense: R{total_prepaid_expense:.2f}")
        yearly_costs_label.config(text="\n".join(yearly_costs))

        # Show disclosures on the financial statements
        display_income_statement(straight_line_lease_expense)  # Use the straight-line lease expense
        display_balance_sheet(total_prepaid_expense, total_accrued_expense)

    except ValueError:
        lease_expense_label.config(text="Error: Please enter valid numeric values.")
        accrued_expense_label.config(text="")
        prepaid_expense_label.config(text="")
        yearly_costs_label.config(text="")
        income_statement_label.config(text="")
        balance_sheet_label.config(text="")

# Function to display formatted Income Statement
def display_income_statement(straight_line_lease_expense):
    # Clear previous content
    for widget in income_statement_frame.winfo_children():
        widget.destroy()

    # Create headers and rows for Income Statement
    tk.Label(income_statement_frame, text="Income Statement", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)
    tk.Label(income_statement_frame, text="Description", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=5)
    tk.Label(income_statement_frame, text="Amount (R)", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=1, column=1, sticky="w", padx=5)

    # Operating Lease Expense (now correctly displays the straight-line lease expense)
    tk.Label(income_statement_frame, text="Operating Lease Expense", bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=5)
    tk.Label(income_statement_frame, text=f"R{straight_line_lease_expense:.2f}", bg="#f0f0f0").grid(row=2, column=1, sticky="w", padx=5)

# Function to display formatted Balance Sheet
def display_balance_sheet(prepaid_expense, accrued_expense):
    # Clear previous content
    for widget in balance_sheet_frame.winfo_children():
        widget.destroy()

    # Create headers and rows for Balance Sheet
    tk.Label(balance_sheet_frame, text="Balance Sheet", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)
    tk.Label(balance_sheet_frame, text="Description", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=5)
    tk.Label(balance_sheet_frame, text="Amount (R)", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=1, column=1, sticky="w", padx=5)

    # Prepaid Expense (Asset)
    tk.Label(balance_sheet_frame, text="Prepaid Expense (Asset)", bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=5)
    tk.Label(balance_sheet_frame, text=f"R{prepaid_expense:.2f}", bg="#f0f0f0").grid(row=2, column=1, sticky="w", padx=5)

    # Accrued Expense (Liability)
    tk.Label(balance_sheet_frame, text="Accrued Expense (Liability)", bg="#f0f0f0").grid(row=3, column=0, sticky="w", padx=5)
    tk.Label(balance_sheet_frame, text=f"R{accrued_expense:.2f}", bg="#f0f0f0").grid(row=3, column=1, sticky="w", padx=5)

# Tkinter GUI Setup
window = tk.Tk()
window.title("Lease Disclosures Calculator")
window.geometry("700x1000")  # Set window size
window.configure(bg="#f0f0f0")  # Set background color

# Create a frame for input fields
input_frame = tk.Frame(window, bg="#f0f0f0", padx=20, pady=20)
input_frame.grid(row=0, column=0, sticky="nsew")

# Input Fields for Lease Information with padding and styling
tk.Label(input_frame, text="Lease Term (Years):", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
entry_lease_term = tk.Entry(input_frame, width=30)
entry_lease_term.grid(row=0, column=1, pady=5)

# Button to dynamically generate fields for yearly installments
generate_button = tk.Button(input_frame, text="Generate Yearly Installments", command=create_yearly_installments, bg="#4CAF50", fg="white", padx=10, pady=5)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)

# Frame to hold yearly installment fields
yearly_frame = tk.Frame(window, bg="#f0f0f0", padx=20, pady=10)
yearly_frame.grid(row=1, column=0, sticky="nsew")

# List to hold references to the yearly installment entry fields
yearly_installments = []

# Error Label (if invalid input for lease term)
error_label = tk.Label(input_frame, text="", bg="#f0f0f0", fg="red")
error_label.grid(row=2, column=0, columnspan=2)

# Button to calculate the total operating lease cost and display financial disclosures
calculate_button = tk.Button(window, text="Calculate and Disclose", command=calculate_operating_lease, bg="#4CAF50", fg="white", padx=10, pady=5)
calculate_button.grid(row=3, column=0, pady=10)

# Result labels for lease expense, accrued expense, prepaid expense, and yearly breakdown
lease_expense_label = tk.Label(window, text="", bg="#f0f0f0", font=("Arial", 10, "bold"))
lease_expense_label.grid(row=4, column=0, sticky="w", pady=5)

accrued_expense_label = tk.Label(window, text="", bg="#f0f0f0", font=("Arial", 10, "bold"))
accrued_expense_label.grid(row=5, column=0, sticky="w", pady=5)

prepaid_expense_label = tk.Label(window, text="", bg="#f0f0f0", font=("Arial", 10, "bold"))
prepaid_expense_label.grid(row=6, column=0, sticky="w", pady=5)

yearly_costs_label = tk.Label(window, text="", bg="#f0f0f0", font=("Arial", 10))
yearly_costs_label.grid(row=7, column=0, sticky="w", pady=5)

# Frame for the Income Statement
income_statement_frame = tk.Frame(window, bg="#f0f0f0", padx=20, pady=10)
income_statement_frame.grid(row=8, column=0, sticky="nsew")

# Frame for the Balance Sheet
balance_sheet_frame = tk.Frame(window, bg="#f0f0f0", padx=20, pady=10)
balance_sheet_frame.grid(row=9, column=0, sticky="nsew")

# Run the Tkinter window
window.mainloop()

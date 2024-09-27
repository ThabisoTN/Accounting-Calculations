import tkinter as tk
from tkinter import ttk

# Function to calculate Present Value of Lease Payments using Annuity Factor
def calculate_present_value(installment, rate, lease_term):
    # Using the Present Value of an Annuity formula
    rate = rate / 100  # Convert percentage to decimal
    return installment * ((1 - (1 + rate) ** -lease_term) / rate)

# Function to calculate Lease Liability and Right of Use Asset
def calculate_lease_liability(installment, deposit, borrowing_rate, lease_term):
    lease_liability = calculate_present_value(installment, borrowing_rate, lease_term)
    right_of_use_asset = lease_liability + deposit  # Right of use asset includes the deposit
    return lease_liability, right_of_use_asset

# Function to calculate Depreciation
def calculate_depreciation(right_of_use_asset, useful_life):
    return right_of_use_asset / useful_life

# Function to create an annual amortization table
def create_amortization_table(lease_liability, installment, borrowing_rate, lease_term):
    amortization_data = []
    remaining_liability = lease_liability
    borrowing_rate = borrowing_rate / 100

    for year in range(1, lease_term + 1):
        interest = remaining_liability * borrowing_rate
        principal = installment - interest
        remaining_liability -= principal
        amortization_data.append({
            "Year": year,
            "Installment": round(installment, 2),
            "Interest": round(interest, 2),
            "Principal": round(principal, 2),
            "Remaining Liability": round(remaining_liability, 2)
        })

    return amortization_data

# Function to display amortization table in the main window using Treeview
def display_amortization_table(amortization_data):
    # Clear previous table if exists
    for row in tree.get_children():
        tree.delete(row)

    # Insert new amortization data into Treeview
    for row in amortization_data:
        tree.insert("", "end", values=(row["Year"], row["Installment"], row["Interest"], row["Principal"], row["Remaining Liability"]))

# Submit Button Logic for GUI
def calculate_leases():
    try:
        # Get user input values
        lease_term = int(entry_lease_term.get())
        useful_life = int(entry_useful_life.get())
        installment = float(entry_installment.get())
        deposit = float(entry_deposit.get())
        borrowing_rate = float(entry_borrowing_rate.get())

        # Calculate Lease Liability and Right of Use Asset
        lease_liability, right_of_use_asset = calculate_lease_liability(installment, deposit, borrowing_rate, lease_term)

        # Calculate Depreciation
        depreciation = calculate_depreciation(right_of_use_asset, useful_life)

        # Create Amortization Table
        amortization_data = create_amortization_table(lease_liability, installment, borrowing_rate, lease_term)

        # Display the results in the main window
        lease_liability_label.config(text=f"Lease Liability: R{lease_liability:.2f}")
        right_of_use_asset_label.config(text=f"Right of Use Asset: R{right_of_use_asset:.2f}")
        depreciation_label.config(text=f"Depreciation per Year: R{depreciation:.2f}")

        # Display the Amortization Table
        display_amortization_table(amortization_data)

    except ValueError:
        lease_liability_label.config(text="Error: Please enter valid numeric values.")
        right_of_use_asset_label.config(text="")
        depreciation_label.config(text="")

# Tkinter GUI Setup
window = tk.Tk()
window.title("Lease Calculator")
window.geometry("600x500")  # Set window size
window.configure(bg="#f0f0f0")  # Set background color

# Create a frame for input fields
input_frame = tk.Frame(window, bg="#f0f0f0", padx=20, pady=20)
input_frame.grid(row=0, column=0, sticky="nsew")

# Input Fields for Lease Information with padding and styling
tk.Label(input_frame, text="Lease Term (Years):", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
entry_lease_term = tk.Entry(input_frame, width=30)
entry_lease_term.grid(row=0, column=1, pady=5)

tk.Label(input_frame, text="Useful Life (Years):", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
entry_useful_life = tk.Entry(input_frame, width=30)
entry_useful_life.grid(row=1, column=1, pady=5)

tk.Label(input_frame, text="Installment (R):", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
entry_installment = tk.Entry(input_frame, width=30)
entry_installment.grid(row=2, column=1, pady=5)

tk.Label(input_frame, text="Deposit (R):", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
entry_deposit = tk.Entry(input_frame, width=30)
entry_deposit.grid(row=3, column=1, pady=5)

tk.Label(input_frame, text="Incremental Borrowing Rate (%):", bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=5)
entry_borrowing_rate = tk.Entry(input_frame, width=30)
entry_borrowing_rate.grid(row=4, column=1, pady=5)

# Calculate Button with padding
calculate_button = tk.Button(input_frame, text="Calculate Lease", command=calculate_leases, bg="#4CAF50", fg="white", padx=10, pady=5)
calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

# Results Labels (Lease Liability, Right of Use Asset, Depreciation)
result_frame = tk.Frame(window, bg="#f0f0f0", padx=20, pady=10)
result_frame.grid(row=1, column=0, sticky="nsew")

lease_liability_label = tk.Label(result_frame, text="", bg="#f0f0f0", font=("Arial", 10, "bold"))
lease_liability_label.grid(row=0, column=0, sticky="w", pady=5)

right_of_use_asset_label = tk.Label(result_frame, text="", bg="#f0f0f0", font=("Arial", 10, "bold"))
right_of_use_asset_label.grid(row=1, column=0, sticky="w", pady=5)

depreciation_label = tk.Label(result_frame, text="", bg="#f0f0f0", font=("Arial", 10, "bold"))
depreciation_label.grid(row=2, column=0, sticky="w", pady=5)

# Amortization Table using Treeview with scrollable area
table_frame = tk.Frame(window, padx=20, pady=10)
table_frame.grid(row=2, column=0, sticky="nsew")

tree = ttk.Treeview(table_frame, columns=("Year", "Installment", "Interest", "Principal", "Remaining Liability"), show="headings")
tree.grid(row=0, column=0, sticky="nsew")

# Add a scrollbar to the Treeview
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

# Define column headings for the amortization table
tree.heading("Year", text="Year")
tree.heading("Installment", text="Installment")
tree.heading("Interest", text="Interest")
tree.heading("Principal", text="Principal")
tree.heading("Remaining Liability", text="Remaining Liability")

# Set column widths
tree.column("Year", width=80)
tree.column("Installment", width=120)
tree.column("Interest", width=120)
tree.column("Principal", width=120)
tree.column("Remaining Liability", width=150)

# Run the Tkinter window
window.mainloop()

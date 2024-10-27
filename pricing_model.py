import pandas as pd

# Load the CSV file containing the natural gas prices
data = pd.read_csv('Nat_Gas.csv')
data['Dates'] = pd.to_datetime(data['Dates'], format='%m/%d/%y')
data.set_index('Dates', inplace=True)

# Function to get the price for a specific date
def get_price_for_date(date):
    date = pd.to_datetime(date)
    if date in data.index:
        return data.loc[date, 'Prices']
    else:
        raise ValueError(f"No price data available for {date}")

# Function to calculate contract value
def price_contract(injection_dates, withdrawal_dates, injection_rate, withdrawal_rate,
                   max_volume, storage_cost_per_month, injection_cost_per_mmbtu, 
                   withdrawal_cost_per_mmbtu, storage_duration_in_months):
    
    # Initialize variables
    total_injected = 0
    total_withdrawn = 0
    total_storage_cost = 0
    total_injection_cost = 0
    total_withdrawal_cost = 0
    total_revenue = 0
    total_cost = 0
    
    # Loop through injection dates
    for date in injection_dates:
        price = get_price_for_date(date)  # Fetch price from CSV data
        volume_to_inject = min(injection_rate, max_volume - total_injected)  # Inject up to max volume
        total_injected += volume_to_inject
        total_injection_cost += volume_to_inject * injection_cost_per_mmbtu
        total_cost += volume_to_inject * price
        total_storage_cost += storage_cost_per_month * storage_duration_in_months  # Storage cost over time
    
    # Loop through withdrawal dates
    for date in withdrawal_dates:
        price = get_price_for_date(date)  # Fetch price from CSV data
        volume_to_withdraw = min(withdrawal_rate, total_injected - total_withdrawn)  # Withdraw only what's stored
        total_withdrawn += volume_to_withdraw
        total_withdrawal_cost += volume_to_withdraw * withdrawal_cost_per_mmbtu
        total_revenue += volume_to_withdraw * price
    
    # Calculate the value of the contract
    contract_value = total_revenue - total_cost - total_storage_cost - total_injection_cost - total_withdrawal_cost
    
    return {
        'Total Injected': total_injected,
        'Total Withdrawn': total_withdrawn,
        'Total Revenue': total_revenue,
        'Total Cost': total_cost,
        'Total Storage Cost': total_storage_cost,
        'Total Injection Cost': total_injection_cost,
        'Total Withdrawal Cost': total_withdrawal_cost,
        'Contract Value': contract_value
    }

# Main function to gather input and display the contract value
def main():
    # Get input from the user
    injection_dates = input("Enter injection dates (comma-separated, e.g., 2023-06-30, 2023-07-31): ").split(", ")
    withdrawal_dates = input("Enter withdrawal dates (comma-separated, e.g., 2023-12-31, 2024-01-31): ").split(", ")
    injection_rate = float(input("Enter the injection rate in MMBtu (e.g., 1e6 for 1 million MMBtu): "))
    withdrawal_rate = float(input("Enter the withdrawal rate in MMBtu (e.g., 1e6 for 1 million MMBtu): "))
    max_volume = float(input("Enter the maximum storage volume in MMBtu (e.g., 5e6 for 5 million MMBtu): "))
    storage_cost_per_month = float(input("Enter the storage cost per month (e.g., 100000 for $100,000 per month): "))
    injection_cost_per_mmbtu = float(input("Enter the injection cost per MMBtu (e.g., 10000 for $10,000 per million MMBtu): "))
    withdrawal_cost_per_mmbtu = float(input("Enter the withdrawal cost per MMBtu (e.g., 10000 for $10,000 per million MMBtu): "))
    storage_duration_in_months = int(input("Enter the storage duration in months (e.g., 6): "))
    
    # Calculate the contract value
    contract_summary = price_contract(injection_dates, withdrawal_dates, injection_rate, withdrawal_rate, 
                                      max_volume, storage_cost_per_month, injection_cost_per_mmbtu, 
                                      withdrawal_cost_per_mmbtu, storage_duration_in_months)
    
    # Display the contract summary
    print("\nContract Summary:")
    print(f"Total Injected: {contract_summary['Total Injected']} MMBtu")
    print(f"Total Withdrawn: {contract_summary['Total Withdrawn']} MMBtu")
    print(f"Total Revenue: ${contract_summary['Total Revenue']:.2f}")
    print(f"Total Cost: ${contract_summary['Total Cost']:.2f}")
    print(f"Total Storage Cost: ${contract_summary['Total Storage Cost']:.2f}")
    print(f"Total Injection Cost: ${contract_summary['Total Injection Cost']:.2f}")
    print(f"Total Withdrawal Cost: ${contract_summary['Total Withdrawal Cost']:.2f}")
    print(f"Contract Value: ${contract_summary['Contract Value']:.2f}")

if __name__ == "__main__":
    main()


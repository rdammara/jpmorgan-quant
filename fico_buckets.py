import pandas as pd

# Function to load data, create FICO buckets, and export as CSV
def process_fico_buckets(file_path, n_buckets=5, output_file="fico_buckets_output.csv"):
    """
    Load data, create FICO score buckets, and export the updated DataFrame to a CSV.
    
    Parameters:
    - file_path: Path to the CSV file containing the data
    - n_buckets: Number of quantile-based buckets to create
    - output_file: Name of the output CSV file
    """
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Define bucket labels where lower labels correspond to better credit scores
    bucket_labels = list(range(n_buckets, 0, -1))  # E.g., for 5 buckets: [5, 4, 3, 2, 1]
    
    # Cut the FICO score into n quantile-based buckets using qcut
    data['fico_rating'] = pd.qcut(data['fico_score'], q=n_buckets, labels=bucket_labels)
    
    # Export the DataFrame to a CSV file
    data[['customer_id', 'fico_score', 'fico_rating']].to_csv(output_file, index=False)
    print(f"Data with FICO buckets exported to {output_file}")

# Example usage
file_path = 'Task 3 and 4_Loan_Data.csv'
process_fico_buckets(file_path, n_buckets=5, output_file="fico_buckets_output.csv")
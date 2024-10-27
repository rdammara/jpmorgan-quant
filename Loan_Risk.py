import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score


data = pd.read_csv('loan_data.csv')
# Preprocessing the data based on the columns you mentioned
def preprocess_data(data):
    # Dropping 'customer_id' since it doesn't contribute to the model
    X = data.drop(['default', 'customer_id'], axis=1)  # Features
    y = data['default']  # Target variable: 0 (no default) or 1 (default)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Scaling the data (optional depending on the model)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test

# Training the RandomForest model
def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)
    return model

# Evaluate model performance
def evaluate_model(model, X_test, y_test):
    y_pred_prob = model.predict_proba(X_test)[:, 1]  # Get probabilities of default (PD)
    auc = roc_auc_score(y_test, y_pred_prob)  # Use AUC-ROC score for evaluation
    print(f"AUC-ROC Score: {auc}")
    return y_pred_prob

# Function to calculate PD (Probability of Default) and expected loss
def calculate_pd_and_expected_loss(model, data, recovery_rate=0.1):
    # Preprocess data
    X_train, X_test, y_train, y_test = preprocess_data(data)
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate model performance
    y_pred_prob = evaluate_model(model, X_test, y_test)
    
    # Predict PD for all customers
    pd = model.predict_proba(data.drop(['default', 'customer_id'], axis=1))[:, 1]
    
    # EAD is the 'loan_amt_outstanding'
    ead = data['loan_amt_outstanding']
    
    # Expected Loss = PD * EAD * (1 - Recovery Rate)
    expected_loss = pd * ead * (1 - recovery_rate)
    
    data['predicted_pd'] = pd
    data['expected_loss'] = expected_loss
    
    return data[['customer_id', 'loan_amt_outstanding', 'expected_loss', 'predicted_pd']]

def export_to_csv(data, file_name="predicted_default_and_loss.csv"):
    """
    Export the DataFrame to a CSV file.

    Parameters:
    - data: DataFrame that contains the predictions and expected loss
    - file_name: Name of the CSV file (default is 'predicted_default_and_loss.csv')
    """
    # Export the DataFrame to a CSV file
    data.to_csv(file_name, index=False)
    print(f"Data exported to {file_name}")

# Example usage:
# After running the prediction and loss calculation
expected_loss_output = calculate_pd_and_expected_loss(model=None, data=data)

# Export the result to CSV
export_to_csv(expected_loss_output, "loan_default_predictions.csv")


expected_loss_output = calculate_pd_and_expected_loss(model=None, data=data)
print(expected_loss_output.head())
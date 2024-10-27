import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt

data = pd.read_csv('Nat_Gas.csv')

#convert the Date column to datetime
data['Dates'] = pd.to_datetime(data['Dates'], format = '%m/%d/%y')

#Set the Dates column as the index for easier time-series analysis
data.set_index('Dates', inplace = True)

# Fit the model using Holt-Winters Exponential Smoothing to capture trends and seasonality
model = ExponentialSmoothing(data['Prices'], trend='add', seasonal='add', seasonal_periods=12).fit()

# Forecast the next 12 months (1 year)
forecast = model.forecast(12)

# Create a new dataframe for the forecasted data
forecast_dates = pd.date_range(start=data.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')
forecast_df = pd.DataFrame({'Prices': forecast}, index=forecast_dates)

# Function to get the price estimate for a given date
def get_price_estimate(input_date):
    # Convert the input date to datetime
    input_date = pd.to_datetime(input_date)
    
    # Check if the input date is in the historical data
    if input_date in data.index:
        price = data.loc[input_date, 'Prices']
        return f"The price of natural gas on {input_date.strftime('%b %Y')} was ${price:.2f}"
    
    # Check if the input date is in the forecasted data
    elif input_date in forecast_df.index:
        price = forecast_df.loc[input_date, 'Prices']
        return f"The estimated price of natural gas on {input_date.strftime('%b %Y')} is ${price:.2f}"
    
    # If the date is out of range, return a message
    else:
        return "The date provided is out of the available range for estimation."

# Example usage
print(get_price_estimate('2025-05-31'))  # Replace with any date you'd like
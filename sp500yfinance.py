import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Download SP500 data with only 'Close' column and auto_adjust=False
ticker = "^GSPC"
data = yf.download(ticker, start="2022-01-01", end="2022-12-31", auto_adjust=False)
monthly_data = data.resample('MS').first()[['Adj Close']]
monthly_data.index.name = 'observation_date'

print(monthly_data.head())
# Reset index to make sure both dataframes have a flat structure
monthly_data.reset_index(inplace=True)

print(monthly_data.columns)
print(monthly_data.head())

# Flatten columns in case of multi-level structure
monthly_data.columns = ['observation_date', 'Adj Close']


# Load interest rate data (replace with your file path)
interest_rate = pd.read_csv("C:/Users/aaziz/Downloads/DFF.csv", parse_dates=['observation_date'], dayfirst=True)
 #Filter interest rate data for 2022 only
interest_rate = interest_rate[(interest_rate['observation_date'] >= '2022-01-01') & (interest_rate['observation_date'] <= '2022-12-31')]

# Align interest rate data to start of the month
interest_rate['observation_date'] = interest_rate['observation_date'] - pd.offsets.MonthBegin(0)

# Ensure datetime and sort for both datasets
monthly_data['observation_date'] = pd.to_datetime(monthly_data['observation_date'])
interest_rate['observation_date'] = pd.to_datetime(interest_rate['observation_date'])

# Merge data on observation_date
combined_data = pd.merge(interest_rate, monthly_data, on='observation_date', how='inner').dropna()

# Calculate changes and growth
combined_data['interest_rate_change'] = combined_data['interest_rate'].diff()
combined_data['sp500_growth'] = combined_data['Adj Close'].pct_change() * 100

# Remove NaN values
combined_data.dropna(subset=['interest_rate_change', 'sp500_growth'], inplace=True)

# Calculate total SP500 return for the year
start_value = monthly_data['Adj Close'].iloc[0]
end_value = monthly_data['Adj Close'].iloc[-1]
total_sp500_return = ((end_value - start_value) / start_value) * 100

# Total interest rate change for the year
start_rate = interest_rate['interest_rate'].iloc[0]
end_rate = interest_rate['interest_rate'].iloc[-1]
total_interest_rate_change = end_rate - start_rate

# Average SP500 growth when interest rate change is positive
positive_interest_growth = combined_data[combined_data['interest_rate_change'] > 0]
avg_sp500_growth = positive_interest_growth['sp500_growth'].mean() if not positive_interest_growth.empty else 0

# Average SP500 growth when interest rate change is negative
negative_interest_growth = combined_data[combined_data['interest_rate_change'] < 0]
avg_sp500_growth_negative = negative_interest_growth['sp500_growth'].mean() if not negative_interest_growth.empty else 0

# Mean of interest rate changes when positive and negative
mean_positive_interest_change = positive_interest_growth['interest_rate_change'].mean() if not positive_interest_growth.empty else 0
mean_negative_interest_change = negative_interest_growth['interest_rate_change'].mean() if not negative_interest_growth.empty else 0

# Display results
print(f"Total SP500 return for 2022: {total_sp500_return:.2f}%")
print(f"Total interest rate change for 2022: {total_interest_rate_change:.2f}")
print(f"Average SP500 growth when interest rate increases: {avg_sp500_growth:.2f}%")
print(f"Average SP500 growth when interest rate decreases: {avg_sp500_growth_negative:.2f}%")
print(f"Mean of interest rate change when positive: {mean_positive_interest_change:.2f}")
print(f"Mean of interest rate change when negative: {mean_negative_interest_change:.2f}")

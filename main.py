import pandas as pd
import numpy as np
from datetime import timedelta, datetime

def calculate_future_value(capital, rate, period):
    return capital * (1 + rate) ** period

def calculate_total_profit(df, capital, start_date, end_date, frequency):
    df_period = df[(df.index >= start_date) & (df.index <= end_date)]

    if frequency == 'day':
        periods = len(df_period)
        rate = df_period['SELIC'].mean() / 100
    elif frequency == 'month':
        df_resampled = df_period.resample('ME').mean()  # Updated here
        periods = len(df_resampled)
        rate = df_resampled['SELIC'].mean() / 100
    elif frequency == 'year':
        df_resampled = df_period.resample('A').mean()
        periods = len(df_resampled)
        rate = df_resampled['SELIC'].mean() / 100
    else:
        raise ValueError("Invalid frequency. Use 'day', 'month' or 'year'.")

    total_profit = calculate_future_value(capital, rate, periods)
    return total_profit

def find_most_profitable_period(df, capital, period_days, start_date, end_date):
    max_profit = -float('inf')
    best_start = None
    best_end = None

    dates = pd.date_range(start=start_date, end=end_date - pd.Timedelta(days=period_days))

    for start in dates:
        end = start + pd.Timedelta(days=period_days)
        profit = calculate_total_profit(df, capital, start, end, 'day')
        if profit > max_profit:
            max_profit = profit
            best_start = start
            best_end = end

    return best_start, best_end, max_profit

def calculate_monthly_profit(df, capital, start_date, end_date):
    df_period = df[(df.index >= start_date) & (df.index <= end_date)]
    df_monthly = df_period.resample('ME').mean()  # Updated here

    print(f"Monthly profit from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}:")

    monthly_profits = []
    for date, row in df_monthly.iterrows():
        rate = row['SELIC'] / 100
        profit = calculate_future_value(capital, rate, 1) - capital
        monthly_profits.append((date.strftime('%m/%Y'), profit))
        print(f"{date.strftime('%m/%Y')} $ {profit:,.2f}")

    return pd.DataFrame(monthly_profits, columns=['Date', 'Profit'])

def format_profit(total_profit):
    return f"${total_profit:,.2f}"

def main():
    dates = pd.date_range(start='2000-01-01', end='2022-03-31', freq='D')
    np.random.seed(0)
    selic_rates = np.random.uniform(low=3.0, high=15.0, size=len(dates))

    df = pd.DataFrame({'SELIC': selic_rates}, index=dates)

    initial_capital = 1500
    period_days = 500
    start_date = pd.to_datetime('2000-01-01')
    end_date = pd.to_datetime('2022-03-31')

    best_start, best_end, profit = find_most_profitable_period(df, initial_capital, period_days, start_date, end_date)

    print("The most profitable period of 500 days from 2000-01-01 to 2022-03-31 was:")
    print(f"Start: {best_start.strftime('%Y-%m-%d')}")
    print(f"End: {best_end.strftime('%Y-%m-%d')}")

    total_profit = calculate_total_profit(df, initial_capital, best_start, best_end, 'day')
    formatted_total_profit = format_profit(total_profit)
    print(f"If I had invested $ {initial_capital} from the beginning of 2000 to March 2022, the profit would be:")
    print(f"{formatted_total_profit}")

    df_monthly_profit = calculate_monthly_profit(df, initial_capital, best_start, best_end)

    total_monthly_profit = df_monthly_profit['Profit'].sum()
    formatted_total_monthly_profit = format_profit(total_monthly_profit)
    print(f"\nTotal monthly profits: {formatted_total_monthly_profit}")

# if teste deletado nao usei mais, det do git tbm OK
if __name__ == "__main__":
    main()

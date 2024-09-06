"""Data preprocessing scripts (handling missing data, cleaning)"""
import pandas as pd

def ohlcv_preprocess(df, start=None, end=None):

    # make sure the data are sorted asc by date and drop anly duplicates. 
    processed_df = df.sort_values(['date']).drop_duplicates(subset=['date']).reset_index(drop=True)

    # Set date as index.
    processed_df.set_index('date', inplace=True)    

    return processed_df[start:end]


def add_common_tech_indicator(data):

    '''price_change: price changes during the trading period '''
    data['price_change'] = data['close'] - data['open']

    '''price_range: price volatilty during the trading period. higher = more volatile '''
    data['price_range'] = data['high'] - data['low']

    '''price_momentum: day-over-day price changes. positive momentum = upward trend, negative=downward trend '''
    data['price_momentum'] = data['close'].diff()

    '''typical_price: average price of the period. '''
    data['typical_price'] = (data['open']+data['high']+data['low']+data['close']) / 4

    '''volume_change (VROC): day-over-day change of trading volume'''
    data['volume_change'] = data['volume'].diff()

    '''Volume Weighted Average Price (VWAP)
    VWAP is a technical analysis indicator that represents the average price a asset has traded at
    throughout the day, weighted by volume. It is calculated by taking the sum of the product of price
    and volume for each trade, divided by the total volume traded for that day.

    Interpretation:
    - Fair value: VWAP can be seen as a benchmark for the "fair price" of an asset during the day.
    - Trend identification: If the current price is above the VWAP, it might suggest an upward trend;
      if below, a downward trend.
    - Trading strategy: Some traders use VWAP as a signal to buy or sell.
      For instance, buying when the price is below the VWAP and selling when it's above.

    Limitations:
    - Lagging indicator: VWAP is a lagging indicator, meaning it reflects past price and volume data.
    - Market conditions: VWAP might not be as effective in highly volatile or illiquid markets.
    '''
    data['vwap'] = (data['typical_price'] * data['volume']).cumsum() / data['volume'].cumsum()


    '''daily_return: day-over-day price changes in % or rate of changes. positive=upward trend, negative=downward-trend
    cummulative_return : total return achieved over a period, considering the compounding of returns.
    calculate by taking the cumulative product of the daily returns plus one (to represent the return for each day).
    '''
    data['daily_return'] = data['close'].pct_change()
    data['cumulative_return'] = (1 + data['daily_return']).cumprod() - 1

    return data 
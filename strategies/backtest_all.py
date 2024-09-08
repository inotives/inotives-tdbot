"""Trading strategy of Crypto Using Moving Average like SMA, EMA, WMA. """
import bt
import talib
import pandas as pd
import data.data_loader as dl 
import matplotlib.pyplot as plt


def signaling_with_simple_SMA(price_data, period, name):
    ''' Strategy: '''

    sma = price_data.rolling(window=period).mean()
    bt_strategy = bt.Strategy(name, [
        bt.algos.SelectWhere(price_data > sma),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance()
    ])

    return bt.Backtest(bt_strategy, price_data)


def signaling_with_SMA_crossover(price_data, pr_short, pr_long, name, plot_graph=False):
    '''Using 2 SMA cross over as signal'''

    sma_short = price_data.rolling(window=pr_short).mean()
    sma_long = price_data.rolling(window=pr_long).mean()

    signals = sma_long.copy()
    signals[sma_short > sma_long] = 1.0
    signals[sma_short < sma_long] = -1.0
    signals[sma_long.isnull()] = 0

    sma_cross = bt.Strategy(name, [
        bt.algos.WeighTarget(signals),
        bt.algos.Rebalance()
    ])

    if(plot_graph):
        # plot the target weights + chart of price & SMAs
        tmp = bt.merge(signals, price_data, sma_short, sma_long)
        tmp.columns = ['signals', 'price', 'sma_short', 'sma_long']
        tmp.plot(figsize=(15,5), secondary_y=['tw'])
        plt.show()
    
    return bt.Backtest(sma_cross, price_data)


def signaling_with_EMA_crossover(price_data, p_short, p_long, name, plot_graph=False):
    '''Details: Using 2 different EMA crossover as signal. Buy: EMA_Short > EMA_long | Sell: EMA_short <'''

    ema_short = talib.EMA(price_data['close'], timeperiod=p_short).to_frame()
    ema_long = talib.EMA(price_data['close'], timeperiod=p_long).to_frame()
    
    # Create a DataFrame to hold the buy/sell signals
    signals = ema_long.copy()
    signals[ema_short > ema_long] = 1.0
    signals[ema_short < ema_long] = -1.0
    signals[ema_long.isnull()] = 0
    signals = signals.rename(columns={0:'close'}) # need this !! make sure col name in data and signals must be the same...


    # Create the strategy
    bt_strategy = bt.Strategy(name, [
        bt.algos.WeighTarget(signals),
        bt.algos.Rebalance()
    ])

    if(plot_graph):
        # plot the target weights + chart of price & SMAs
        tmp = bt.merge(signals, price_data, ema_short, ema_long)
        tmp.columns = ['tw', 'price', 'sma_short', 'sma_long']
        tmp.plot(figsize=(15,5), secondary_y=['tw'])
        plt.show()


    return bt.Backtest(bt_strategy, price_data)

def signaling_with_ADX(price_data, period, name, adx_threshold=20):
    '''Signal backtest with ADX (Average Directional Index). BUY: ADX > Threshold, SELL: ADX < Threshold '''
    
    # Ensure price_data has the necessary columns: 'high', 'low', 'close'
    if not all(col in price_data.columns for col in ['high', 'low', 'close']):
        raise ValueError("price_data must contain 'high', 'low', and 'close' columns")
    
    adx = talib.ADX(price_data['high'], price_data['low'], price_data['close'], timeperiod=period).to_frame() 
    adx.rename(columns={adx.columns[0]: 'adx'}, inplace=True)
    
    close_price = price_data[['close']]

    adx['signal'] = 0
    adx.loc[adx['adx'] > adx_threshold, 'signal'] = 1
    adx.loc[adx['adx'] < adx_threshold, 'signal'] = -1
    adx.loc[adx['adx'] == 0, 'signal'] = 0

    signals = adx[['signal']].rename(columns={'signal':'close'})

    # Define your strategy
    bt_strategy = bt.Strategy(name, [
        bt.algos.WeighTarget(signals),
        bt.algos.Rebalance()
    ])

    return bt.Backtest(bt_strategy, close_price)


def signaling_with_Bollinger(price_data, period, name, num_std=2):
    """
    Create buy/sell signals based on Bollinger Bands for a mean reversion strategy.

    price_data: DataFrame with 'close' prices
    period: the lookback period for Bollinger Bands calculation
    name: strategy name
    num_std: number of standard deviations to define the bands (default 2)
    """
    
    # Ensure price_data contains the necessary 'close' column
    if 'close' not in price_data.columns:
        raise ValueError("price_data must contain a 'close' column")
    
    # Calculate Bollinger Bands using TA-lib
    upper_band, middle_band, lower_band = talib.BBANDS(price_data['close'], timeperiod=period, nbdevup=num_std, nbdevdn=num_std, matype=0)
    

    # Fill any NaN values in bands with the first valid value
    upper_band = upper_band.fillna(method='bfill')
    middle_band = middle_band.fillna(method='bfill')
    lower_band = lower_band.fillna(method='bfill')

    # Create signals DataFrame with buy (1) and sell (-1) signals
    bband = price_data.copy()
    bband['signal'] = 0
    bband.loc[ bband['close'] < lower_band, 'signal' ] = -1
    bband.loc[ bband['close'] > upper_band, 'signal' ] = 1

    signals = bband[['signal']].rename(columns={'signal': 'close'})

    # Define your strategy
    bt_strategy = bt.Strategy(name, [
        bt.algos.WeighTarget(signals),
        bt.algos.Rebalance()
    ])

    return bt.Backtest(bt_strategy, price_data)
    




def signaling_with_RSI(price_data, period, name, rsi_overbought=70, rsi_oversold=30):
    """
    Create buy/sell signals based on RSI levels using TA-lib and `bt`.
    
    price_data: DataFrame with 'close' prices
    period: the lookback period for RSI calculation
    name: strategy name
    rsi_overbought: threshold for overbought RSI (default 70)
    rsi_oversold: threshold for oversold RSI (default 30)
    """

    # Ensure price_data contains the necessary 'close' column
    if 'close' not in price_data.columns:
        raise ValueError("price_data must contain a 'close' column")
    
    # Calculate RSI
    rsi = talib.RSI(price_data['close'], timeperiod=period).to_frame()
    rsi.rename(columns={rsi.columns[0]: 'rsi'}, inplace=True)

    rsi['signal'] = 0
    
    # Buy signal when RSI is below the oversold threshold
    rsi.loc[rsi['rsi'] < rsi_oversold, 'signal' ] = 1
    
    # Sell signal when RSI is above the overbought threshold
    rsi.loc[rsi['rsi'] > rsi_overbought, 'signal' ] = -1

    signals = rsi[['signal']].rename(columns={'signal': 'close'})

    bt_strategy = bt.Strategy(name, [
        bt.algos.WeighTarget(signals),
        bt.algos.Rebalance()
    ])

    return bt.Backtest(bt_strategy, price_data)
    

    


def buy_n_hold(price_data, name):
    '''Details: Buy once and then hold. treated as benchmark strategy. '''
    
    # buy once and hold - use this as benchmark
    bt_strategy = bt.Strategy(name, [
        bt.algos.RunOnce(),
        bt.algos.SelectAll(),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance()
    ])

    return bt.Backtest(bt_strategy, price_data)



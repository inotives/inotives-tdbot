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



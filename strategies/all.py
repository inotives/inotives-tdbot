"""Trading strategy of Crypto Using Moving Average like SMA, EMA, WMA. """
import bt
import talib
import pandas as pd
import data.data_loader as dl 
import matplotlib.pyplot as plt


def signaling_with_SMA(price_data, period, name):
    
    sma = price_data.rolling(window=period).mean()
    bt_strategy = bt.Strategy(name, [
        bt.algos.SelectWhere(price_data > sma),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance()
    ])

    return bt.Backtest(bt_strategy, price_data)

def signaling_with_EMA_crossover(price_data, p_short, p_long, name):
    EMA_short = talib.EMA(price_data['close'], timeperiod=p_short).to_frame()
    EMA_long = talib.EMA(price_data['close'], timeperiod=p_long).to_frame()

    # Create a DataFrame to hold the buy/sell signals
    signals = EMA_long.copy()
    signals[EMA_long.isnull()] = 0

    # Buy signal (1) when EMA_short crosses above EMA_long
    signals[EMA_short > EMA_long] = 1
    
    # Sell signal (-1) when EMA_short crosses below EMA_long
    signals[EMA_short < EMA_long] = -1

    # Create the strategy
    bt_strategy = bt.Strategy(name, [
        bt.algos.WeighTarget(signals),
        bt.algos.Rebalance()
    ])
    
    return bt.Backtest(bt_strategy, price_data)

def buy_n_hold(price_data, name):
    
    # buy once and hold - use this as benchmark
    bt_strategy = bt.Strategy(name, [
        bt.algos.RunOnce(),
        bt.algos.SelectAll(),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance()
    ])

    return bt.Backtest(bt_strategy, price_data)



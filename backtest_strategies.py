import bt
import matplotlib.pyplot as plt
import data.data_loader as dl
import strategies.backtest_all as st


ohlcv_df = dl.load_crypto_ohlcv_from_db('Bitcoin', 365)
closing_price = ohlcv_df[['close']]
adx_input = ohlcv_df[['high', 'low', 'close']]

# Trying out strategy
# sma20 = st.signaling_with_SMA(closing_price, 20, 'sma20')
# sma50 = st.signaling_with_SMA(closing_price, 50, 'sma50')
# sma100 = st.signaling_with_SMA(closing_price, 100, 'sma100')

sma_cross = st.signaling_with_SMA_crossover(closing_price, 7, 28, 'SMA_CROSS:7D,28D')
ema_cross = st.signaling_with_EMA_crossover(closing_price, 7, 28, 'EMA_CROSS:7D,28D')

adx_25 = st.signaling_with_ADX(adx_input, 14, 'ADX14:25Threshold', adx_threshold=25)
adx_20 = st.signaling_with_ADX(adx_input, 14, 'ADX14:20Threshold', adx_threshold=20)
adx_30 = st.signaling_with_ADX(adx_input, 14, 'ADX14:30Threshold', adx_threshold=30)

bband = st.signaling_with_Bollinger(closing_price, 14, 'BBAND:14D')

benchmark = st.buy_n_hold(closing_price, 'BENCHMARK:BuynHold')

bt_results = bt.run(sma_cross, ema_cross,adx_20, adx_25, adx_30, bband, benchmark)
bt_results.plot(title='strategy comparison')
plt.show()



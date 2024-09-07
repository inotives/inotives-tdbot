import bt
import matplotlib.pyplot as plt
import data.data_loader as dl
import strategies.all as st




ohlcv_df = dl.load_crypto_ohlcv_from_db('Bitcoin', 365)
closing_price = ohlcv_df[['close']]
adx_input = ohlcv_df[['high', 'low', 'close']]

# Trying out strategy
# sma20 = st.signaling_with_SMA(closing_price, 20, 'sma20')
# sma50 = st.signaling_with_SMA(closing_price, 50, 'sma50')
# sma100 = st.signaling_with_SMA(closing_price, 100, 'sma100')

# sma_cross = st.signaling_with_SMA_crossover(closing_price, 7, 28, 'SMA_CROSS')
# ema_cross = st.signaling_with_EMA_crossover(closing_price, 7, 28, 'EMA_CROSS')

adx_25 = st.signaling_with_ADX(adx_input, 14, 'adx_25', adx_threshold=25)
adx_20 = st.signaling_with_ADX(adx_input, 14, 'adx_20', adx_threshold=20)
adx_30 = st.signaling_with_ADX(adx_input, 14, 'adx_30', adx_threshold=30)

benchmark = st.buy_n_hold(closing_price, 'benchmark')

bt_results = bt.run(adx_20, adx_25, adx_30, benchmark)
bt_results.plot(title='strategy comparison')
plt.show()



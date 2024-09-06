import bt
import matplotlib.pyplot as plt
import data.data_loader as dl
import strategies.all as st




ohlcv_df = dl.load_crypto_ohlcv_from_db('Bitcoin', 365)
closing_price = ohlcv_df[['close']]

# Trying out strategy
sma20 = st.signaling_with_SMA(closing_price, 20, 'sma20')
sma50 = st.signaling_with_SMA(closing_price, 50, 'sma50')
sma100 = st.signaling_with_SMA(closing_price, 100, 'sma100')
benchmark = st.buy_n_hold(closing_price, 'benchmark')

bt_results = bt.run(sma20, sma50, sma100, benchmark)
bt_results.plot(title='optimization')
plt.show()


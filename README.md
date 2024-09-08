# inotives-tdbots

This repos record my experiment with backtesting lib (bt) and TA-lib to simulate backtesting strategies with OHLCV crypto data. 
After refining the backtesting, next would be to work on implementing them into bots or create those into dashboards to present as summarize startegy. 

## Trading Strategis Implemented
Here are the few trading strategies i am working on this repo:

#### Trend Following Strategy
*"The trend is your friend."* 
Strategy that aims to capitalize on the momentum of asset price movements, assuming that the price will continue in its current direction—whether upward or downward. Using this strategy typically enter positions when we are seeing a trend is forming (Uptrend) and exit when the trend reverses (Downtrend). 
Common indicators: 
- Moving Average, 50-Days and 200-Days
- Moving Average Convergence Divergence (MACD)
- ADX

#### Mean Reversion Strategy
The strategy that based on the idea that asset prices tend to revert to their historical mean (average) over time. This strategy assumes that when the price deviates significantly from its average, it will eventually return, creating a trading opportunity. Prices fluctuate around a long-term mean, and extreme movements are often followed by reversions back to the mean.
Buy when price drop below historical average, Sell then price raise above its average. 
Common Indicators: 
- RSI
- Bollinger Bands

#### Breakout Strategy 
A breakout strategy focuses on entering a trade when the price breaks out of a defined range, such as support or resistance levels. The idea is to capitalize on increased volatility that typically follows a breakout. Buy when the price breaks above resistance, or sell when it breaks below support.
Common Indicators: 
- Price Patterns (e.q: triangles, flags)
- Pivot points
- Volume analysis
  
## Other Strategies that plan to work on

#### Scalping Strategy (wip)
A scalping strategy involves making a large number of small, quick trades throughout the day. The goal is to capture very small price movements in a short time. Profit from small price changes over a brief period, typically using leverage to amplify returns.

#### Arbitrage Strategy (wip)
An arbitrage strategy takes advantage of price differences between markets or exchanges. Traders buy an asset in one market where the price is lower and sell it in another market where the price is higher, profiting from the difference. Capitalize on price inefficiencies between two markets or asset classes.
- Entry point: When a price discrepancy is detected between two exchanges.
- Exit point: Close both trades simultaneously to lock in the price difference.
- Common types: Spatial arbitrage (between different exchanges), statistical arbitrage (based on mean reversion between asset prices).

#### Momentum Strategy (wip)
A momentum strategy is based on the idea that strong price movements in one direction are likely to continue for some time. The strategy typically involves buying assets that have shown an upward momentum or short-selling those with downward momentum. Assets that are moving strongly in one direction are more likely to continue moving in that direction.
- Entry point: Buy assets with upward momentum, sell assets with downward momentum.
- Exit point: Close the position when the momentum shows signs of weakening or reversing.
- Common indicators: RSI, MACD, Moving Averages, Momentum Indicator.

#### Pairs Trading (wip)
A pairs trading strategy involves taking long and short positions simultaneously on two highly correlated assets. The goal is to profit from the temporary divergence in their price movement. Two correlated assets are expected to move together; when they diverge, they should revert.
- Entry point: Buy the underperforming asset and short the outperforming asset.
- Exit point: Close both positions when the price relationship returns to the mean.
- Common indicators: Correlation, cointegration tests.

#### Swing Trading Strategy (wip)
A swing trading strategy looks to capture short- to medium-term price movements. Traders hold positions for several days to weeks, trying to profit from price "swings" within a trend. Capture gains from small trends or corrections within a larger trend.
- Entry point: Buy during price pullbacks in an uptrend or sell during rallies in a downtrend.
- Exit point: Close the position when the price reaches a target or reverses direction.
- Common indicators: Moving averages, Fibonacci retracement, trend lines, and oscillators (e.g., RSI).

#### News-Based Trading (wip)
A news-based strategy leverages market-moving news or economic events to inform trading decisions. Traders react to breaking news, earnings reports, or other major events that can drive significant price movements.News events create volatility and price movements that traders can capitalize on.
- Entry point: Enter trades after a market-moving news release.
- Exit point: Exit when the price stabilizes or after a set profit target.
- Common news sources: Economic calendars, earnings reports, government policies, geopolitical events.







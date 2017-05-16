To download historical Apple prices: `./download_prices.py aapl -o aapl.csv`

To price a call option: `./price_option.py aapl.csv`

Default parameters are a strike price equal to its current value with a risk free return of 3%.
The option is written at the middle of historical data for an estimation date at the end of historical data.
Volatility is estimated on the first half of historical data using standard deviation.

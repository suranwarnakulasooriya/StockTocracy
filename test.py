from init import *
from datetime import datetime

price_history = yf.Ticker('AAPL').history(period='2y', # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                   interval='1wk', # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                   actions=False)

time_series = list((price_history['High']+price_history['Low'])/2) # average of high and low

dt_list = [datetime.fromtimestamp(pendulum.parse(str(dt)).float_timestamp) for dt in list(price_history.index)]
print(dt_list)

plt.style.use('dark_background')
plt.plot(dt_list, time_series, linewidth=2)
plt.show()
plt.close()
import os
import datetime
import pandas_datareader as web

# https://pandas-datareader.readthedocs.io/en/latest/remote_data.html

today_str = str(datetime.date.today())

today_y = int(today_str[:4])
today_m = int(today_str[5:7])
today_d = int(today_str[8:])

#print(today_y)
#print(today_m)
#print(today_d)


#print(str(datetime.date.today()))

os.environ["ALPHAVANTAGE_API_KEY"] = "pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

f = web.DataReader(["USD/JPY"], "av-forex",
api_key=os.getenv('ALPHAVANTAGE_API_KEY'))


print(f)

#stock.loc["2022-09-01"]

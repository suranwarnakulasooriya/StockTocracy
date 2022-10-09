import yfinance as yf # get stock information
import pendulum # parsing stuff from yf

#import matplotlib.pyplot as plt

# dict that matches symbols to company names
stock_lookup = {
    'AAPL':'Apple Inc.',
    'MSFT':'Microsoft Corporation',
    'GOOG':'Alphabet Inc. Class C',
    'GOOGL':'Alphabet Inc. Class A',
    'AMZN':'Amazon Inc.',
    'TSLA':'Tesla Inc.',
    'BBY':'Best Buy Co. Inc',
    'UNH':'UnitedHealth Group Inc.',
    'JNJ':'Johnson & Johnson',
    'XOM':'Exxon Mobil Corporation',
    'V':'Visa Inc.',
    'TSM':'Taiwan Semiconductor Manufacturing Company Ltd.',
    'META':'Meta Platforms Inc.',
    'WMT':'Wallmart Inc.',
    'CVX':'Chevron Corporation',
    'JPM':'JP Morgan Chase & Co.',
    'LLY':'Eli Lilly and Company',
    'NVDA':'NVIDIA Corporation',
    'PG':'Proctor and Gamble Company',
    'HD':'Home Depot Inc.',
    'MA':'Mastercard Inc.',
    'BAC':'Bank of America Corporation',
    'ABBV':'AbbVie Inc.',
    'PFE':'Pfizer Inc.',
    'KO':'Coca Cola Company',
    'NVO':'Novo Nordisk',
    'PEP':'PepsiCo Inc.',
    'MRK':'Merck and Company Inc.',
    'BABA':'Alibaba Group',
    'COST':'Costco Wholesale Corporation',
    'TMO':'Thermo Fisher Scientific Inc.',
    'DHR':'Danaher Corporation',
    'AVGO':'Broadcom Inc.',
    'TM':'Toyota Motor Corporation',
    'SHEL':'Royal Dutch Shell PLC',
    'ABT':'Abott Laboratories',
    'DIS':'Walt Disney Company',
    'TMUS':'T-Mobile US Inc.',
    'MCD':"McDonald's Corporation",
    'ORCL':'Oracle Corporation',
    'CSCO':'Cisco Systems Inc.',
    'WFC':'Wells Fargo & Company',
    'VZ':'Verizon Communications Inc.',
    'COP':'ConocoPhillips',
    'NEE':'NextEra Energy Inc.',
    'TXN':'Texas Instruments Inc.',
    'SCHW':'Charles Schwab Corporation',
    'UPS':'United Parcel Service Inc.',
    'NKE':'Nike Inc.',
    'MS':'Morgan Stanley',
    'ADBE':'Adobe Inc.',
    'PM':'Phillip Morris International Inc.',
    'CMCSA':'Comcast Corporation',
    'RTX':'Raytheon Technologies Corporation',
    'RY':'Royal Bank of Canada',
    'AMGN':'Amgen Inc.',
    'LOW':"Lowe's Companies Inc.",
    'UNP':'Union Pacific Corporation',
    'CVS':'CVS Health Corporation',
    'HON':'Honeywell International Inc.',
    'LMT':'Lockheed Martin Corporation',
    'T':'AT&T Inc.',
    'INTC':'Intel Corporation',
    'PYPL':'PayPal Holdings Inc.',
    'GS':'Goldman Sachs Group Inc.',
    'NFLX':'Netflix Inc.',
    'SBUX':'Starbucks Corporation',
    'SNY':'Sanofi ADS',
    'AMD':'Advanced Micro Devices Inc.',
    'CAT':'Catterpillar Inc.',
    'BUD':'Anheuser-Busch',
    'BLK':'BlackRock Inc.',
    'BTI':'British American Tobacco Industries',
    'SONY':'Sony Group Corporation',
    'BA':'Boeing Company',
    'NOC':'Northrup Grumman Corporation',
    'GE':'General Electric Company',
    'TGT':'Target Corporation',
    'ABNB':'Airbnb Inc.',
    'WM':'Waste Management Inc.',
    'ATVI':'Activision Blizzard Inc.',
    'CSX':'CSX Corporation',
    'UBER':'Uber Technologies',
    'MUFG':'Mitsubishi UFJ',
    'F':'Ford Motor Company',
    'GM':'General Motors Company',
    'MNST':'Moster Beverage Corporation',
    'MRNA':'Moderna Inc.',
    'HSY':'Hershey Company',
    'GIS':'General Mills Inc.',
    'ADSK':'Autodesk Inc.',
    'CMG':'Chipotle Mexican Grill Inc.',
    'KHC':'Kraft Heinz Company',
    'FDX':'FedEx Corporation',
    'HMC':'Honda Motor Company',
    'MSI':'Motorolla Solutions Inc.',
    'TWTR':'Twitter Inc.',
    'COF':'Capital One Financial Corporation',
    'SHOP':'Shopify Inc.',
    'EA':'Electronic Arts Inc.',
    'RACE':'Ferrari',
}

# split stock_lookup
stock_symbols = list(stock_lookup.keys())
stock_names = list(stock_lookup.values())

class StockSpectator:
    def __init__(self):
        self.current_view = 'AAPL' # the stock being currently viewed in the plotly ui
        self.stocks = dict.fromkeys(stock_lookup,0) # dict of all stocks (keys = stock symbols, values = number of shares)

    def load(self,filename): # load save data
        with open(filename,'r') as f: held_stocks = f.read().splitlines() # load
        for stock in held_stocks: self.stocks[stock[:-2]] = int(stock[-1]) # write to stock attribute
    
    def get_stocks(self): # return dict of stocks with nonzero shares
        nonzeroes = {}
        for stock in self.stocks:
            if self.stocks[stock] != 0:
                nonzeroes[stock] = self.stocks[stock]
        return nonzeroes

SS = StockSpectator()

#print(stock_symbols)
#test = StockSpectator()
#test.load('stocks.txt')
#test.get_stocks()
#print(test.get_stocks())
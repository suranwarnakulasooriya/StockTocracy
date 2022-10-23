import yfinance as yf # get stock information
import pendulum # parsing stuff from yf
from numpy.random import normal
from random import randint, choice
from datetime import datetime as date
from pandas import date_range as dr

#import matplotlib.pyplot as plt
today_y = date.today().year; today_m = date.today().month; today_d = date.today().day
datelist = dr(date(today_y-1,today_m,today_d),date(today_y,today_m,today_d),freq='D')
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
    'UBER':'Uber Technologies Inc.',
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
    'ZM':'Zoom Video Communications Inc',
    'NOK':'Nokia Corporation',
    'SIRI':'Sirius XM Holdings Inc.',
    'CAJ':'Canon Inc.',
    'EBAY':'eBay Inc.',
    'DAL':'Delta Air Lines Inc.',
    'FRC':'First Republic Bank',
    'LUV':'Southwest Airlines',
    'DB':'Deutsche Bank',
    'SPOT':'Spotify Technologies',
    'EXPE':'Expedia Group',
    'MDB':'MongoDB Inc.',
    'DPZ':"Domino's Pizza Inc."
}

# split stock_lookup
stock_symbols = list(stock_lookup.keys())
stock_names = list(stock_lookup.values())

def get_365_days(price_history):
    #price_history = yf.Ticker(symbol).history(period='1y',interval='1d',actions=False)
    L = list(round((price_history['High']+price_history['Low'])/2,2))
    #del price_history
    index = 0
    while len(L) < 365:
        index -= 3
        L.insert(index,round((L[index-1]+L[index+1])/2,2))
    return L

class StockSpectator:
    def __init__(self):
        self.current_view = 'AAPL' # the stock being currently viewed in the plotly ui
        #self.allstocks = dict.fromkeys(stock_lookup,[0 for _ in range(365)]) # dict of all stocks (keys = stock symbols, values = number of shares)
        #self.allstocks = self.load('stocks.txt')
        #self.heldstocks = self.get_stocks()
        self.allstocks = {}
        self.allstocks = self.load_shares(self.allstocks,'stocks.txt')
        self.heldstocks = self.filter_stocks(self.allstocks)
        self.budget = self.load_budget('budget.txt')
        self.selfstocks = {}
        self.selfstocks = self.load_shares(self.selfstocks,'selfshares.txt')
        self.selfshares = self.filter_stocks(self.selfstocks)

    #def load(self,filename:str): # load save data
    #    with open(filename,'r') as f: held_stocks = f.read().splitlines() # load
    #    for stock in held_stocks: self.allstocks[stock[:-2]] = int(stock[-1]) # write to stock attribute
    #    return self.allstocks

    def load_shares(self,destination,filename:str):
        with open(filename,'r') as f:
            stock_histories = f.read().splitlines()
        stock_histories = [line.split() for line in stock_histories]
        #for s in stock_histories:
        #    s = [int(i) for i in s]
        stock_histories = [[int(i) for i in s] for s in stock_histories]
        destination = dict(zip(stock_symbols,stock_histories))
        return destination        

    def load_budget(self,filename:str) -> float:
        with open(filename,'r') as f:
            self.budget = float(f.read().strip())
        return self.budget

    def filter_stocks(self,source): # return dict of stocks with nonzero shares
        nonzeroes = {}
        for stock in source:
            if source[stock].count(0) != 365:
                nonzeroes[stock] = source[stock]
        return nonzeroes
        
    def dummyvote(self,symbol,autovoters:int=4,day:int=1):
        #self.allstocks[symbol][-day] = randint(0,50)
        #self.selfstocks[symbol][-day] = randint(0,50)
        self.allstocks[symbol][-day] = 1
        self.selfstocks[symbol][-day] = 1
        self.heldstocks = self.filter_stocks(self.allstocks)
        self.selfshares = self.filter_stocks(self.selfstocks)

    def vote(self,symbol,autovoters:int=4,uservote:int=0,day:int=1,document:bool=False):
        shares = self.allstocks[symbol][-day] # get number of shares
        
        price = price_history = yf.Ticker(symbol).history(period='1d',interval='1d',actions=False)
        price = round((float(price['High'])+float(price['Low']))/2,2) # share price is avg of high and low of most recent price

        ma = int(int(self.budget//price)) # maximum volume that can be bought
        uservote = (max(-shares,min(uservote,ma)))
        votes = [str(uservote)] # list of votes
        for voter in range(autovoters): votes.append(str(max(-shares,min(int(normal(0,(shares+20)**1.5)),ma)))) # autovote
        vote = round(sum([int(v) for v in votes])/(len(votes)**1)) # final decision is avg
        if document:
            print(f'vote on {stock_lookup[symbol]}')
            print(f'budget               : ${self.budget}')
            print(f'held shares          : {shares}')
            print(f"share price of {symbol} {' '*(5-len(symbol))}: ${price}")
            print(f'held price           : ${round(shares*price,2)}')
            print(f'maximum buy volume   : {ma} (-${round(ma*price,2)})')
            print(f'maximum sell volume  : {shares} (+${round(shares*price,2)})')
            print(f'range                : {-shares} ... {ma}')
            print(f'voters               : {autovoters+1}')
            print(f'user vote            : {uservote}')
            print(f'votes                : {" ".join(votes)}')
            print(f'decision             : {str(vote)} ',end='')
            if vote == 0: print('(hold)')
            elif vote < 0: print('(sell)')
            else: print('(buy)')
        delta = round(vote*price,2)
        self.budget -= delta # apply change to delta
        self.budget = round(self.budget,2) # round off budget
        self.selfstocks[symbol][-day] = shares + uservote # apply user's vote to their personal record
        a = shares + uservote
        shares += vote # apply decision to group shares
        b = shares
        self.allstocks[symbol][-day] = shares # save new share number
        if document:
            print(f'new shares           : {shares} ',end='')
            if vote >= 0: print(f'(+{vote})')
            else: print(f'({vote})')
            print(f'budget               : ${self.budget} ',end='')
            if delta > 0: print(f'(-${abs(delta)})')
            else: print(f'(+${abs(delta)})')

        self.heldstocks = self.filter_stocks(self.allstocks)
        self.selfshares = self.filter_stocks(self.selfstocks)
        #print(uservote,vote)
        #print(b==a)
        #print(self.heldstocks == self.selfshares)
        #print(uservote == vote)
        #print(self.selfshares)




 
SS = StockSpectator()

#print(SS.selfshares)

#for day in range(1):
#    for stock in ['AAPL','GOOGL']:
#        SS.dummyvote(stock,day=day)

#print(SS.heldstocks['AAPL'])
#print(len(SS.heldstocks['AAPL']))
#for day in range(100):
#    for stock in ['AAPL']:#,'GOOGL','TSLA','KO','F','SNY']:
#        print(day,stock)
#        SS.vote(stock,choice([2,4,6,8,10,12,14,16,18,20,22,24,26,28]),randint(-50,50),day=day+1,document=False)
#price_history = yf.Ticker('AAPL').history(period='1d',interval='1d',actions=False)
#print(list(price_history.index))
#axis = [datetime.fromtimestamp(pendulum.parse(str(dt)).float_timestamp) for dt in list(price_history.index)]
#print(axis)
r = 365
#print(len(SS.allstocks['AAPL']))
#SS.allstocks['AAPL'] = [randint(1,1) for _ in range(r)]
#SS.selfstocks['AAPL'] = [randint(2,2) for _ in range(r)]
#SS.allstocks['TSLA'] = [randint(1,1) for _ in range(r)]
#SS.selfstocks['TSLA'] = [randint(2,2) for _ in range(r)]
#for i in range(r): SS.allstocks['AAPL'][i] = randint(1,1)
#for i in range(r): SS.selfstocks['AAPL'][i] = randint(2,2)
for i in range(r): SS.allstocks['TSLA'][i] = 1#randint(1,1)
for i in range(r): SS.selfstocks['TSLA'][i] = 2#randint(2,2)
for i in range(r): SS.allstocks['AAPL'][i] = 1#randint(1,1)
for i in range(r): SS.selfstocks['AAPL'][i] = 2#randint(2,2)

#SS.selfstocks['HD'][0] = 1

SS.heldstocks = SS.filter_stocks(SS.allstocks)
SS.selfshares = SS.filter_stocks(SS.selfstocks)

#print(SS.allstocks['AAPL'])
#print(SS.heldstocks)
#print(SS.selfshares)






#print(len(bruh))
#bruh = fill(bruh)
#print()
#print(len(bruh))


#print(len(bruh))
#print(price_history['High'])
#print(price_history['Open'])

#print(price_history)

#print(SS.allstocks['AAPL'])
#print(SS.selfstocks['AAPL'])

#print(SS.heldstocks['AAPL'][2])
#print(SS.budget)
#SS.vote(choice(stock_symbols),choice([2,4,6,8,10,12,14,16,18,20,22,24,26]),document=True)

#print(SS.allstocks)

#print(SS.allstocks)
#print(SS.get_stocks())
#SS.heldstocks = SS.get_stocks()
#print(SS.heldstocks)

#print(stock_symbols)
#test = StockSpectator()
#test.load('stocks.txt')
#test.get_stocks()
#print(test.get_stocks())
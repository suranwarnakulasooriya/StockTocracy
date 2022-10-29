import yfinance as yf # get stock information
import pendulum # parsing stuff from yf
from numpy.random import normal
from random import randint, choice
from random import uniform
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
    def __init__(self,d,m,y):
        self.current_view = 'AAPL' # the stock being currently viewed in the plotly ui
        #self.allstocks = dict.fromkeys(stock_lookup,[0 for _ in range(365)]) # dict of all stocks (keys = stock symbols, values = number of shares)
        #self.allstocks = self.load('stocks.txt')
        #self.heldstocks = self.get_stocks()
        self.redate = False
        self.datestr = f'{d}/{m}/{y}'
        self.lag = 0
        self.allstocks = {}
        self.allstocks = self.load_shares('stocks.txt')
        self.heldstocks = self.filter_stocks(self.allstocks)
        self.budget = self.load_budget('budget.txt')
        self.sbudg = self.load_budget('sbudg.txt')
        self.selfstocks = {}
        self.selfstocks = self.load_shares('selfshares.txt')
        self.symbolvotes = self.load_voted('votes.txt')
        self.selfshares = self.filter_stocks(self.selfstocks)
        self.voted = False
        self.votes = []
        self.vote = 0
        self.toc = 0
        self.namesb = ['Mason','John','Abby','Phillip','Raj','Rika','Juan-Paul','Yara','Abdul','Giuseppe','Michael','Ria','Margaret','Chloe','Anna','Layla',
        'Noah','Clark','Fred','Josh','Allison','Rachel','Marcus','Jason','Mahmoud','Sai','Tori','Frederick','Quandale','Alexander','Stanislow','Benjamin',
        'Tanaka','Trenton','Katherine','Trevor','Rilley','Muhammed','Kawasaki','Kumar','Anura','James','Louis','Peter','Griffith','Sangakar','Boris','Nina',
        'Jerry','Kraemer','Jaqueline','Hannah','Petrov','Arkhipov','Charles','Ahmed','Hamza']
        self.names = self.namesb[:]
        self.sc = 0
        self.hist = []
        self.hist = self.load_hist('hist.txt')

    def save(self,gs:str,ss:str,gb:str,sb:str,v:str,g:str):
        with open(gs,'w') as f:
            for sym in stock_symbols:
                f.write(' '.join([str(i) for i in self.allstocks[sym]])); f.write('\n')
        with open(ss,'w') as f:
            for sym in stock_symbols:
                f.write(' '.join([str(i) for i in self.selfstocks[sym]])); f.write('\n')
        with open(gb,'w') as f: f.write(str(self.budget))
        with open(sb,'w') as f: f.write(str(self.sbudg))
        with open(v,'w') as f:
            f.write(self.datestr); f.write('\n')
            for sym in stock_symbols:
                f.write(str(self.symbolvotes[sym])); f.write('\n')
        with open(g,'w') as f:
            for h in self.hist:
                f.write(str(h)); f.write('\n')

    def load_hist(self,filename:str):
        with open(filename,'r') as f:
            L = f.read().splitlines()
        return [int(i) for i in L]

    def load_shares(self,filename:str):
        with open(filename,'r') as f:
            stock_histories = f.read().splitlines()
        stock_histories = [line.split() for line in stock_histories]
        if self.redate:
            for i,e in enumerate(stock_histories):
                e.pop(0)
                e.append(e[-1])
                stock_histories[i] = e
        stock_histories = [[int(i) for i in s] for s in stock_histories]
        destination = dict(zip(stock_symbols,stock_histories))
        return destination        

    def load_budget(self,filename:str) -> float:
        with open(filename,'r') as f:
            budget = float(f.read().strip())
        return budget

    def load_voted(self,filename:str):
        D = {}
        f = open(filename,'r')
        votes = f.read().splitlines()[1:]
        votes = [int(vote) for vote in votes]
        f.close()
        f = open(filename,'r')
        s = f.read()[:10]
        if s != self.datestr:
            self.redate = True
        f.close()
        D = dict(zip(stock_symbols,votes))
        return D

    def filter_stocks(self,source): # return dict of stocks with nonzero shares
        nonzeroes = {}
        for stock in source:
            if source[stock].count(0) != 365:
                nonzeroes[stock] = source[stock]
        return nonzeroes

    def uivote(self,vote,autovoters:int=8):
        self.vote = int(vote[:vote.index(' ')])
        self.votes = []
        self.toc
        price_history = yf.Ticker(self.current_view).history(period='3mo',interval='1d',actions=False)
        L = list(round((price_history['High']+price_history['Low'])/2,2))
        shares = self.allstocks[self.current_view][-1]
        price = L[-1]
        M = self.budget // price
        inc = 0
        dec = 0
        for i in range(len(L)):
            try:
                if L[i] < L[i+1]:
                    inc += abs(L[i]-L[i+1])
                else: dec += abs(L[i]-L[i+1])
            except IndexError: pass
        r = inc + dec
        avg = (inc-dec)/2 
        for _ in range(8):
            vote = max(-shares,min(M, round(normal(-avg,r/5))))
            n = randint(0,len(self.names)-1)
            self.votes.append((self.names[n],vote))
            self.names.pop(n)
        self.toc = round((sum([v[1] for v in self.votes])+self.vote)/9)
        self.names = self.namesb[:]
        self.budget -= self.toc*price
        self.budget = round(self.budget,2)
        self.allstocks[self.current_view][-1] = self.toc
        self.selfstocks[self.current_view][-1] = self.vote
        self.heldstocks = self.filter_stocks(self.allstocks)
        self.selfshares = self.filter_stocks(self.selfstocks)
        self.sbudg -= self.vote*price
        self.sbudg = round(self.sbudg,2)
        self.hist.append(self.vote-self.toc)

    def demo(self):
        S = randint(2,15)
        mu = randint(-10,10)
        sig = randint(5,20)
        self.budget = round(uniform(10_000,1_000_000),2)
        self.sbudg = round(uniform(10_000,1_000_000),2)
        for s in range(S):
            self.current_view = stock_symbols[s]
            for d in range(randint(30,365)):
                self.allstocks[self.current_view][-d-1] = int(normal(15,3))
                self.selfstocks[self.current_view][-d-1] = int(normal(15,3))
                self.hist.append(int(normal(mu,sig)))
        SS.heldstocks = SS.filter_stocks(SS.allstocks)
        SS.selfshares = SS.filter_stocks(SS.selfstocks)

SS = StockSpectator(today_d,today_m,today_y)

SS.heldstocks = SS.filter_stocks(SS.allstocks)
SS.selfshares = SS.filter_stocks(SS.selfstocks)


SS.demo()
from alpha_vantage.timeseries import TimeSeries
import yfinance as yf
import matplotlib.pyplot as plt 
import pandas as pd
import json
import csv
import os

'''
important attributes to know:
    name = company name
    asset = ticker
    price = most recent close
    fd = all fundamentals
    marketcap = market cap
    beta = beta
    sector = sector
'''



class FinancialAsset:
    '''
    I want this to act as the parent class for crypto/FX/who knows what later,
    for now it will model a financial asset (stock), 
    it should have attributes like price as well as fundamental data
    '''

    def __init__(self, asset):
        '''init atts'''
        self.asset = asset
        self.__LOAD_DATA()
        self.__SAVE_DATA()
    

    def __LOAD_DATA(self):
        '''load the timeseries and fundamentals'''
        # check if the path exists, if not, create folder
        if not os.path.exists(f'asset_data/{self.asset.lower()}'):
            os.makedirs(f'asset_data/{self.asset.lower()}')

        try:    
            data = f'asset_data/{self.asset}/{self.asset}_timeseries.csv'
            fundamentals = f'asset_data/{self.asset}/{self.asset}_fundamentals.json'

            with open(data, 'r') as f:
                # read the csv data and then sort to chronological order
                self._RAW_DATA = pd.read_csv(f, index_col=0)
                self._RAW_DATA.sort_index(axis=0)

            # set price to the most recent quote
            self.price = self._RAW_DATA['4. close'][0]

            with open(fundamentals, 'r') as f:
                self.fd = pd.read_json(f, orient='index')

            # set fundamentals now that it is loaded
            self.__SET_FUNDAMENTALS(True)

        except:
            print(f'No data found for {self.asset.upper()}, retrieving data...')

            self._RAW_DATA, self.meta_data = self.__GET_TIMESERIES()
            self._RAW_DATA.sort_index(axis=0)
            self.price = self._RAW_DATA['4. close'][-1]

            fndmt = self.__GET_FUNDAMENTALS()
            # if fundamnetals are available, set values
            if fndmt == True:
                self.__SET_FUNDAMENTALS(True)


    def __GET_TIMESERIES(self):
        '''retrieve timeseries data'''
        ts = TimeSeries(key='R4NLQ9F769D3AH9W', output_format='pandas')

        _RAW_DATA, meta_data = ts.get_daily(symbol=self.asset, outputsize='full')
        _RAW_DATA.sort_index(axis=0)

        return _RAW_DATA, meta_data


    def __GET_FUNDAMENTALS(self):
        '''retrieve marketcap'''
        try:
            fund = yf.Ticker(self.asset)

            self.fd = pd.DataFrame.from_dict(fund.info, orient='index')
            self.fd.reset_index(inplace=True)
            self.fd.columns = ["Attribute", "Recent"]

            return True

        except:
            # i would rather not go through the trouble of no fundamentals;
            # i need their market cap and beta for certain calculations
            print(f'No fundamental information available for {self.asset.upper()}.')
            print('Recommended to remove asset from portfolio.')
            
            return False


    def __SET_FUNDAMENTALS(self, tf=False):
        '''set fundamentals if company overview works'''
        if tf == True:
            self.fd.set_index('Attribute', inplace=True)
            self.name = self.fd.loc['shortName', 'Recent']
            self.marketcap = self.fd.loc['marketCap', 'Recent']
            self.sector = self.fd.loc['sector', 'Recent']
            self.beta = self.fd.loc['beta', 'Recent']
            self.fd.reset_index(inplace=True)
            self.fd.columns = ["Attribute", "Recent"]

        else:
            self.name = None
            self.marketcap = None
            self.sector = None
            self.beta = None



    def __SAVE_DATA(self):
        '''save the price + fundamental data into a csv + json'''
        fd = self.fd.to_dict(orient='index')
        self._RAW_DATA.to_csv(f'asset_data/{self.asset.lower()}/{self.asset.lower()}_timeseries.csv')

        with open(f'asset_data/{self.asset.lower()}/{self.asset.lower()}_fundamentals.json', 'w') as f:
            json.dump(fd, f)


    def plot(self):
        '''plot daily chart w/1 yr time frame'''
        self._RAW_DATA['4. close'].sort_index(axis=0).tail(365).plot()

        plt.title(f'{self.asset.upper()} Daily Time Series')
        plt.xticks(rotation='30', wrap=True)
        plt.grid()
        plt.show()
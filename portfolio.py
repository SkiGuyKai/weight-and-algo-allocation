import pandas as pd 
import numpy as np 
from financial_asset import FinancialAsset
from sector_analysis import SectorAnalysis
from security_analysis import SecurityAnalysis
import matplotlib.pyplot as plt
from alpha_vantage.sectorperformance import SectorPerformances


# i would like a master dict that contains important metrics
# ex. {'asset' : symbol, 'returns' : df['returns'], ...}
# perhaps this master dict will be the final result, it could include
# each weight and rules and all that, then it could be sent to the main
# or sent to trade logic where it the data is then accessed and evaluated

# CURRENTLY wokring on security analysis to import back here 
# and send to weight module, then ultimately devise position strategies


'''
How to access portfolio financial assets:
   pf.portfolio['TICKER'][0]

   eh just look at the __CREATE_PORTFOLIO function

'''


class Portfolio:
    '''
    Manages the portfolio positions and weights,
    ideally this will also put out a graphical representation
    '''
    manager = 'Kai Casterline'

    def __init__(self, assets):
        self.assets = [asset.upper() for asset in assets]
        self._PORTFOLIO_WEIGHTS = []
        self._TOT_WEIGHT = 0
        self.tot_marketcap = 0
        self.portfolio = self.__CREATE_PORTFOLIO()
        self.__GET_WEIGHTS()
        self.__SECTOR_CALC()
        self.__SECURITY_CALC()


    def __CREATE_PORTFOLIO(self):
        '''retrieve asset price and marketcap'''
        portfolio = {}
        for asset in self.assets:
            fa = FinancialAsset(asset)
            portfolio[asset] = [fa, fa._RAW_DATA, fa.fd]

        return portfolio

    # this will be moved into weight module eventually
    # weight module will syntehsize all weight params (sector+security RS, beta)
    # final weights will be brought back into the portfolio
    def __GET_WEIGHTS(self):
        '''calculate the weights of each asset'''
        for data in self.portfolio.values():
            self.tot_marketcap += int(data[0].marketcap)
        
        for data in self.portfolio.values():
            data[0].weight = round(int(data[0].marketcap)/self.tot_marketcap, 4)
           
            if data[0].weight > 0.20:
                data[0].weight = 0.20
            elif data[0].weight < 0.05:
                data[0].weight = 0.05

            self._PORTFOLIO_WEIGHTS.append(data[0].weight)
            self._TOT_WEIGHT += data[0].weight
        if self._TOT_WEIGHT < 1.0:
            self._CASH_WEIGHT = 1.0 - self._TOT_WEIGHT
            self.assets.append('Cash')
            self._PORTFOLIO_WEIGHTS.append(self._CASH_WEIGHT)

    # this will be moved into security analysis module eventually
    def get_returns(self):
        '''calc the returns of the portfolio'''


    def __SECTOR_CALC(self):
        '''send assets through sector analysis'''
        sector_strength = SectorAnalysis(self.portfolio)
        self.portfolio['SECTOR_STRENGTH'] = sector_strength


    def __SECURITY_CALC(self):
        '''send assets and sector performance through security analysis'''
        security_strength = SecurityAnalysis(self.portfolio)


    def piefolio(self):
        '''show the pie chart portfolio breakdown'''
        plt.pie(self._PORTFOLIO_WEIGHTS, labels=self.assets, shadow=True, 
            autopct='%1.2f%%')
        plt.show()


    def plot_chart(self):
        '''plot the chart of the portfolio'''
        for data in self.portfolio.values():
            data.plot()


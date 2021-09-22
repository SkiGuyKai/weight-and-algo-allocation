import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from financial_asset import FinancialAsset
from sector_analysis import SectorAnalysis
from security_analysis import SecurityAnalysis
from weight import Weight
from alpha_vantage.sectorperformance import SectorPerformances


class Portfolio:
    '''
    Manages the portfolio positions and weights,
    ideally this will also put out a graphical representation
    '''
    manager = 'Kai Casterline'

    def __init__(self, assets):
        self.assets = [asset.upper() for asset in assets]
        self.portfolio = self.__CREATE_PORTFOLIO()
        self.__SECTOR_CALC()
        self.__SECURITY_CALC()
        self.__GET_WEIGHTS()


    def __CREATE_PORTFOLIO(self):
        '''retrieve asset price and marketcap'''
        portfolio = {}
        for asset in self.assets:
            fa = FinancialAsset(asset)
            portfolio[asset] = [fa, fa._RAW_DATA]

        return portfolio

    # this will be moved into weight module eventually
    # weight module will syntehsize all weight params (sector+security RS, beta)
    # final weights will be brought back into the portfolio
    def __GET_WEIGHTS(self):
        '''calculate the weights of each asset'''
        self.weight = Weight(self.portfolio, self.sector_strength.asp)
        self.assets.append('CASH')

    # this will be moved into security analysis module eventually
    def get_returns(self):
        '''calc the returns of the portfolio'''


    def __SECTOR_CALC(self):
        '''send assets through sector analysis'''
        self.sector_strength = SectorAnalysis(self.portfolio)


    def __SECURITY_CALC(self):
        '''send assets and sector performance through security analysis'''
        self.security_strength = SecurityAnalysis(self.portfolio, self.sector_strength.asp)


    def piefolio(self):
        '''show the pie chart portfolio breakdown'''
        weights = []
        for asset in self.portfolio.values():
            if asset in self.assets:
                weights.append(asset[0].weight)
            else:
                weights.append(self.portfolio['CASH'])

        print(weights)

        plt.pie(weights, labels=self.assets, shadow=True, 
            autopct='%1.2f%%')
        plt.show()


    def plot_chart(self):
        '''plot the chart of the portfolio'''
        for data in self.portfolio.values():
            if data[0].name not in self.assets:
                pass
            else:
                data[0].plot()

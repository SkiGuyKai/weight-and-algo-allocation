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


    def __SECTOR_CALC(self):
        '''send assets through sector analysis'''
        self.sector_strength = SectorAnalysis(self.portfolio)


    def __SECURITY_CALC(self):
        '''send assets and sector performance through security analysis'''
        self.security_strength = SecurityAnalysis(self.portfolio, self.sector_strength.asp)


    def __GET_WEIGHTS(self):
        '''calculate the weights of each asset'''
        self.weight = Weight(self.portfolio, self.sector_strength.asp)
        #self.assets.append('CASH')


    def __GET_RETURNS(self):
        '''calc the returns of the portfolio'''
        pass
        

    def piefolio(self):
        '''show the pie chart portfolio breakdown'''
        weights = [asset[0].weight for asset in self.portfolio.values()]

        plt.pie(weights, labels=self.assets, shadow=True, 
            autopct='%1.2f%%', normalize=False)
        plt.show()


    def plot_chart(self, col='4. close', returns=False):
        '''plot the chart of the portfolio'''
        for data in self.portfolio.values():
            data[0].plot(col, returns)

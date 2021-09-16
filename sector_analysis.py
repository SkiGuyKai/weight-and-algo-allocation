import matplotlib.pyplot as plt
from alpha_vantage.sectorperformance import SectorPerformances
import pandas as pd 
from sector_finder import Translator 


# GOALS:
# - effective plotting and visualization of trends



# Important Attributes and Methods:
#     rank(number) creates df w/top sectors based on strength
#     plot_sectors(df) plots bar chart showing sector performances
#     _RAW_SECTORS is the df containing all sector data
#     asp is the df containing only sectors within the portfolio
#     portfolio_sectors is a list of sectors within the portfolio



class SectorAnalysis:
    '''
    this class will handle the calculations of relevant sectors,
    i'm still deciding on if i will do bottom-up or top-down portfolio
    '''

    def __init__(self, portfolio):
        '''init atts'''
        self.portfolio = portfolio
        self._RAW_SECTORS = self.__SECTOR_PERFORMANCE()
        self.__RS()
        self.asp = self.__ASSET_SECTOR_PERFORMANCE()

    def __SECTOR_PERFORMANCE(self):
        '''track the sector performance'''
        sp = SectorPerformances(key='R4NLQ9F769D3AH9W', output_format='pandas')
        data, meta_data = sp.get_sector()
        _RAW_SECTORS = data[['Rank B: Day Performance', 'Rank C: Day Performance', 'Rank D: Month Performance']]

        return _RAW_SECTORS


    def __RS(self):
            '''calculate the RS of each sector using the following equation:
            RS = 0.6(Rank D)+0.25(Rank C)+0.15(Rank B)'''
            temp = self._RAW_SECTORS.mul([0.15, 0.25, 0.6] , axis='columns')
            self._RAW_SECTORS.loc[:, 'Strength'] = temp.sum(axis=1)


    def __ASSET_SECTOR_PERFORMANCE(self):
        '''check sector performance for each asset'''
        temp_sectors = [asset[0].sector for asset in self.portfolio.values()]

        # translate portfolio sectors first!
        translated_sectors = Translator(temp_sectors)
        self.portfolio_sectors = translated_sectors.translated

        # selecting rows based on condition
        asp = self._RAW_SECTORS.loc[self.portfolio_sectors]

        return asp


    def plot_sectors(self, data):
        '''plot the sector performance'''
        data.plot(kind='bar', sharey=True, rot=45,
            title='Sector Performance', grid=True)
        plt.show()


    def rank(self, number):
        '''rank the sectors in order of relative strength'''
        self.top_sectors = self._RAW_SECTORS.nlargest(number, 'Strength')

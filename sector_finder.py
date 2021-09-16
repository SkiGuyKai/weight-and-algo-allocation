class Translator:
    '''Use this to easily translate yfinance sectors to alpha_vantage'''

    def __init__(self, portfolio_sectors):
        '''take in all sector names'''
        self._TRANSLATOR = ['Information Technology', 'Communication Services',
        'Health Care', 'Real Estate', 'Consumer Discretionary', 'Consumer Staples',
        ' Energy', 'Financials', 'Industrials', 'Materials', 'Utilities']

        self._TRANSLATE = ['Technology', 'Communication Services', 'Healthcare',
        'Real Estate', 'Consumer Cyclical', 'Consumer Defensive', 'Energy',
        'Financial Services', 'Industrials', 'Basic Materials', 'Utilities']

        self.portfolio_sectors = portfolio_sectors

        self.translated = []

        self.__TRANSLATE()


    def __TRANSLATE(self):
        '''defines the dict that our translations come from'''
        for from_s in self.portfolio_sectors:
            x = 0
            for to_s in self._TRANSLATE:
                if from_s != to_s:
                    x += 1
                elif from_s == to_s:
                    if self._TRANSLATOR[x] in self.translated:
                        x = 0
                    else:
                        self.translated.append(self._TRANSLATOR[x])
                        x = 0
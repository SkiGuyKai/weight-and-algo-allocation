import matplotlib.pyplot as plt 
import pandas as pd 


# I want this to contain the security RS in a dict or dataframe, probably df 
# it should also plot the RS of the security along side the sector RS


class SecurityAnalysis:
    '''
    This class calculates the relative strength of a security against
    its sector's performance
    '''

    def __init__(self, portfolio):
        '''init important atts and data'''
        self.portfolio = portfolio


    def locate(self):
        '''locate sector related to each security'''
        



from portfolio import Portfolio

pf = Portfolio(['AMZN','AAPL','IBM','NVDA','AMD','MRNA','JPM'])
pf.portfolio['SECTOR_STRENGTH'].rank(5)
print(pf.portfolio['SECTOR_STRENGTH'].top_sectors.loc[:, ['Rank D: Month Performance', 'Strength']] * 100)
print(pf.portfolio['AMZN'][1]['4. close'])
print(pf.portfolio['AMZN'][2].iloc[0:25])
print(pf.portfolio['SECTOR_STRENGTH'].asp)








'''Here's what the master dictionary should look like:
dict = {'TICKER' : [fa object, df containing all data]}'''
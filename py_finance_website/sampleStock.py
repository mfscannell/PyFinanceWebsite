from py_finance import YahooFinanceClient
from py_finance import InvestorsUtilities

def showIndex(ticker):
    print(ticker)
    stockClient = YahooFinanceClient(ticker)
    stockHistory = stockClient.getHistory('2017-05-30', '2017-07-28')
    stockHistory.calcInvestorsData()
    stockHistory.calcDayReturn(10)
    stockHistory.calcDayReturn(20)
    stockHistory.calcDayReturn(30)
    stockHistory.printToScreen()
    #stockHistory.writeToCsvFile('sAndP.csv')

showIndex('^DJT')
print('*******************')
showIndex('^DJI')
print('*******************')
showIndex('^GSPC')
print('*******************')
showIndex('^IXIC')
#showIndex('cern')

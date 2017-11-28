from py_finance import YahooFinanceClient
from py_finance import InvestorsUtilities

def showIndex(ticker, startDate, endDate):
    print(ticker)
    stockClient = YahooFinanceClient(ticker)
    stockHistory = stockClient.getHistory(startDate, endDate)
    stockHistory.calcInvestorsData()
    stockHistory.printToScreen()

# stockSymbol = input("Enter stock symbol:")
# startDate = input("Start date (yyyy-mm-dd):")
# endDate = input("End date (yyyy-mm-dd):")
#
# if stockSymbol == "all":
#     showIndex('^DJT', startDate, endDate)
#     print('*******************')
#     showIndex('^DJI', startDate, endDate)
#     print('*******************')
#     showIndex('^GSPC', startDate, endDate)
#     print('*******************')
#     showIndex('^IXIC', startDate, endDate)
# else:
#     showIndex(stockSymbol, startDate, endDate)

thing1 = '2017-11-30'
thing2 = '2017-11-29'
thing3 = '2018-01-01'

print(thing1 == thing2)
print(thing1 >= thing2)
print(thing1 >= thing3)

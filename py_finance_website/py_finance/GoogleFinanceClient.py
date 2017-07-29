import datetime
import urllib

class GoogleFinanceClient:
    def __init__(self, tickerSymbol):
        self.tickerSymbol = tickerSymbol.upper()
    def printStock(self):
        print(self.tickerSymbol)
    def getHistory(self, fromDate, toDate):
        startDate = datetime.date(int(fromDate[0:4]),int(fromDate[5:7]),int(fromDate[8:10]))
        endDate = datetime.date(int(toDate[0:4]),int(toDate[5:7]),int(toDate[8:10]))
        print(startDate)
        print(endDate)
        print(startDate.strftime('%b %d, %Y'))
        print(endDate.strftime('%b %d, %Y'))
        url_string = "http://www.google.com/finance/historical?q={0}".format(self.tickerSymbol)
        url_string += "&startdate={0}&enddate={1}&output=csv".format(startDate.strftime('%b %d, %Y'),endDate.strftime('%b %d, %Y'))
        print(url_string)
        csv = urllib.urlopen(url_string).readlines()
        csv.reverse()
        return csv
        #for bar in xrange(0,len(csv)-1):
        #    ds,open_,high,low,close,volume = csv[bar].rstrip().split(',')
        #    open_,high,low,close = [float(x) for x in [open_,high,low,close]]
        #    dt = datetime.datetime.strptime(ds,'%d-%b-%y')
        #    self.append(dt,open_,high,low,close,volume)

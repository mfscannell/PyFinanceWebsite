from py_finance.InvestorsUtilities import InvestorsUtilities
import csv

class StockHistory:
    def __init__(self, stockHistoryString):
        self.tradingDays = stockHistoryString.split('\n')

        keys = self.tradingDays[0].split(',')
        self.tradingDays = self.tradingDays[1:]

        iTradingDays = 0

        while iTradingDays < len(self.tradingDays):
           if self.tradingDays[iTradingDays] == '' or 'null' in self.tradingDays[iTradingDays]:
               del self.tradingDays[iTradingDays]
           else:
               tempTradingDay = self.tradingDays[iTradingDays].split(',')
               self.tradingDays[iTradingDays] = {}

               for j, item in enumerate(tempTradingDay):
                    if keys[j] == 'Date':
                        self.tradingDays[iTradingDays]['Date'] = item
                    elif keys[j] == 'Volume':
                        self.tradingDays[iTradingDays]['Volume'] = float(item)
                    else:
                        self.tradingDays[iTradingDays][keys[j]] = {'Price': float(item)}

               iTradingDays = iTradingDays + 1
    def calcDayReturn(self, numDays):
        for i, tradingDay in enumerate(self.tradingDays):
            endIndex = min(i + numDays, len(self.tradingDays) - 1)
            endDay = self.tradingDays[endIndex]
            self.tradingDays[i][str(numDays) + ' Day Return'] = (endDay['Close']['Price'] - tradingDay['Close']['Price']) / tradingDay['Close']['Price']
    def calcInvestorsData(self):
        print('calcInvestorsData')
        for i, tradingDay in enumerate(self.tradingDays):
            self.__determineDistributionDay(i)
            self.__determineFollowThroughDay(i)
            self.__determineNumDistributionDays(i)
            self.__determineResistancePrice(i)
        pass
    def printToScreen(self):
        for i, item in enumerate(self.tradingDays):
            if i == len(self.tradingDays) - 25:
                print('--------------')

            printString = str(len(self.tradingDays) - i) + '. '

            if 'Date' in item:
                printString += item['Date'] + ','

            if 'Volume' in item:
                printString += str(item['Volume']) + ','

            if 'Adj Close' in item and 'Price' in item['Adj Close']:
                printString += str(item['Adj Close']['Price']) + ','

            if 'IsDistributionDay' in item:
                printString += str(item['IsDistributionDay']) + ','

            if 'IsFollowThroughDay' in item:
                printString += str(item['IsFollowThroughDay']) + ','

            if 'NumDistributionDays' in item:
                printString  += str(item['NumDistributionDays']) + ','

            if 'SupportPrice' in item:
                printString += str(item['SupportPrice']) + ','

            if 'ResistancePrice' in item:
                printString += str(item['ResistancePrice']) + ','

            print(printString)
    def writeToCsvFile(self, fileName):
        keys = [
            'Date',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Is Distribution Day',
            'Is Follow Through Day',
            'Num Distribution Days',
            'SupportPrice',
            'ResistancePrice',
            '10 Day Return',
            '20 Day Return',
            '30 Day Return'
        ]

        with open(fileName, 'wb') as csvFile:
            writer = csv.writer(csvFile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(keys)

            for tradingDay in self.tradingDays:
                writer.writerow([
                    tradingDay['Date'],
                    tradingDay['Open']['Price'],
                    tradingDay['High']['Price'],
                    tradingDay['Low']['Price'],
                    tradingDay['Close']['Price'],
                    tradingDay['Volume'],
                    tradingDay['IsDistributionDay'],
                    tradingDay['IsFollowThroughDay'],
                    tradingDay['NumDistributionDays'],
                    tradingDay['SupportPrice'],
                    tradingDay['ResistancePrice'],
                    tradingDay['10 Day Return'],
                    tradingDay['20 Day Return'],
                    tradingDay['30 Day Return']
                ])
    def __determineDistributionDay(self, index):
        if index > 0:
            self.tradingDays[index]['IsDistributionDay'] = InvestorsUtilities.isDistributionDay(self.tradingDays[index], self.tradingDays[index - 1])
        else:
            self.tradingDays[index]['IsDistributionDay'] = False
    def __determineFollowThroughDay(self, index):
        if index >= 7:
            self.tradingDays[index]['IsFollowThroughDay'] = self.__isDay7(index) or self.__isDay6(index) or self.__isDay5(index) or self.__isDay4(index)
        else:
            self.tradingDays[index]['IsFollowThroughDay'] = False

        if index == 0:
            self.tradingDays[index]['SupportPrice'] = 0
        elif 'SupportPrice' not in self.tradingDays[index]:
            i = index - 1

            while i > 0 and self.tradingDays[index]['Close']['Price'] < self.tradingDays[i]['SupportPrice']:
                i  = i - 1

            self.tradingDays[index]['SupportPrice'] = self.tradingDays[i]['SupportPrice']
    def __determineNumDistributionDays(self, index):
        j = index
        followThroughDayEncountered = False
        self.tradingDays[index]['NumDistributionDays'] = 0

        while j > 0 and j >= index - 24 and not self.tradingDays[j]['IsFollowThroughDay']:
            if self.tradingDays[j]['IsDistributionDay'] and self.tradingDays[index]['High']['Price'] < 1.06 * self.tradingDays[j]['Close']['Price']:
                self.tradingDays[index]['NumDistributionDays'] = self.tradingDays[index]['NumDistributionDays'] + 1

            j = j - 1
    def __determineResistancePrice(self, index):
        if index == 0:
            self.tradingDays[index]['ResistancePrice'] = self.tradingDays[index]['High']['Price']
        else:
            self.tradingDays[index]['ResistancePrice'] = max(self.tradingDays[index - 1]['ResistancePrice'], self.tradingDays[index]['High']['Price'])
    def __isDay4(self, index):
        establishedLowPrice = 0
        todaysDate = self.tradingDays[index]['Date']

        if self.__isHigherVolumeGain(index):
            if self.__isDay1(index - 3):
                establishedLowPrice = min(self.tradingDays[index - 3]['Low']['Price'], self.tradingDays[index - 4]['Low']['Price'])

                if self.tradingDays[index - 1]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 2]['Low']['Price'] > establishedLowPrice:
                    self.tradingDays[index]['SupportPrice']  = establishedLowPrice
                    return True
            else:
                return False

        return False
    def __isDay5(self, index):
        establishedLowPrice = 0

        if self.__isHigherVolumeGain(index):
            if self.__isDay1(index - 4):
                establishedLowPrice = min(self.tradingDays[index - 4]['Low']['Price'], self.tradingDays[index - 5]['Low']['Price'])

                if self.tradingDays[index - 1]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 2]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 3]['Low']['Price'] > establishedLowPrice:
                    self.tradingDays[index]['SupportPrice']  = establishedLowPrice
                    return True
            else:
                return False

        return False
    def __isDay6(self, index):
        establishedLowPrice = 0

        if self.__isHigherVolumeGain(index):
            if self.__isDay1(index - 5):
                establishedLowPrice = min(self.tradingDays[index - 5]['Low']['Price'], self.tradingDays[index - 6]['Low']['Price'])

                if self.tradingDays[index - 1]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 2]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 3]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 4]['Low']['Price'] > establishedLowPrice:
                    self.tradingDays[index]['SupportPrice']  = establishedLowPrice
                    return True
            else:
                return False

        return False
    def __isDay7(self, index):
        establishedLowPrice = 0

        if self.__isHigherVolumeGain(index):
            if self.__isDay1(index - 6):
                establishedLowPrice = min(self.tradingDays[index - 6]['Low']['Price'], self.tradingDays[index - 7]['Low']['Price'])

                if self.tradingDays[index - 1]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 2]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 3]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 4]['Low']['Price'] > establishedLowPrice and \
                   self.tradingDays[index - 5]['Low']['Price'] > establishedLowPrice:
                    self.tradingDays[index]['SupportPrice']  = establishedLowPrice
                    return True
            else:
                return False

        return False
    def __isDay1(self, index):
        day1Range = self.tradingDays[index]['High']['Price'] - self.tradingDays[index]['Low']['Price']

        return self.tradingDays[index]['Close']['Price'] > 0.9 * day1Range + self.tradingDays[index]['Low']['Price'] or \
               self.tradingDays[index]['Close']['Price'] > self.tradingDays[index - 1]['Low']['Price']
    def __isHigherVolumeGain(self, index):
        return self.tradingDays[index]['Volume'] > self.tradingDays[index - 1]['Volume'] and \
               self.tradingDays[index]['Close']['Price'] > 1.01 * self.tradingDays[index - 1]['Close']['Price']

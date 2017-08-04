class InvestorsUtilities:
    @staticmethod
    def isDistributionDay(tradingDay, previousTradingDay):
        volDiff = tradingDay['Volume'] > previousTradingDay['Volume']
        priceDiff = tradingDay['Adj Close'] < 0.998 * previousTradingDay['Adj Close']

        return volDiff and priceDiff

    @staticmethod
    def isFollowThroughDay(tradingDay, previousTradingDay):
        return tradingDay['Adj Close'] > 1.01 * previousTradingDay['Adj Close'] and tradingDay['Volume'] > previousTradingDay['Volume']

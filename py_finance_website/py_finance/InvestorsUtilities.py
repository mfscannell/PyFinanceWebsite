class InvestorsUtilities:
    @staticmethod
    def isDistributionDay(tradingDay, previousTradingDay):
        volDiff = tradingDay['Volume'] > previousTradingDay['Volume']
        priceDiff = tradingDay['Adj Close']['Price'] < 0.998 * previousTradingDay['Adj Close']['Price']

        return volDiff and priceDiff

    @staticmethod
    def isFollowThroughDay(tradingDay, previousTradingDay):
        return tradingDay['Adj Close']['Price'] > 1.01 * previousTradingDay['Adj Close']['Price'] and tradingDay['Volume'] > previousTradingDay['Volume']

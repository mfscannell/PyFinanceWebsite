var StockUtilities = {
    /**
     * Calculates the Open-High-Low-Close and Volume data arrays.
     **/
    calcOhlcVolume: function(tradingDaysData) {
        var ohlc = [];
        var volume = [];

        for (var i = 0; i < tradingDaysData.length; i++) {
            ohlc.push([
                Date.parse(tradingDaysData[i]['Date']),
                tradingDaysData[i]['Open'],
                tradingDaysData[i]['High'],
                tradingDaysData[i]['Low'],
                tradingDaysData[i]['Close']
            ]);

            volume.push([
                Date.parse(tradingDaysData[i]['Date']),
                tradingDaysData[i]['Volume']
            ]);
        }

        return {
            'ohlc': ohlc,
            'volume': volume
        };
    },
    getSeries: function(stockSymbol,
                        ohlc,
                        volume,
                        upperTechlicalIndicators,
                        lowerTechnicalIndicators) {
        groupingUnits = [[
                'week',
                [1]
            ], [
                'month',
                [1, 2, 3, 4, 6]
            ]];

        var series = [{
            name: stockSymbol,
            type: 'candlestick',
            id: 'primary',
            data: ohlc,
            dataGrouping: {
                units: groupingUnits
            }
        },
        {
            type: 'column',
            name: 'Volume',
            data: volume,
            yAxis: 1,
            dataGrouping: {
                units: groupingUnits
            }
        }];

        for (var i = 0; i < lowerTechnicalIndicators.length; i++) {
            if (lowerTechnicalIndicators[i].indicatorType === 'RSI') {
                series.push(StockUtilities.getRsiSeries(ohlc,
                                                        lowerTechnicalIndicators[i].interval));
            }
        }

        for (var i = 0; i < upperTechlicalIndicators.length; i++) {
            if (upperTechlicalIndicators[i].indicatorType === 'SMA') {
                series.push(StockUtilities.getSmaSeries(ohlc, upperTechlicalIndicators[i].interval));
            } else if (upperTechlicalIndicators[i].indicatorType === 'EMA') {
                series.push(StockUtilities.getEmaSeries(ohlc, upperTechlicalIndicators[i].interval));
            }
        }

        return series;
    },
    /**
     * Returns the series for the Exponential Moving Average.
     **/
    getEmaSeries: function(ohlc, dayMovingAvg) {
        var multiplier = (2 / (dayMovingAvg + 1));
        var emaData = [];

        for (var j = dayMovingAvg - 1; j < ohlc.length; j++) {
            if (j === dayMovingAvg - 1) {
                var total = 0;

                for (var k = 0; k < dayMovingAvg; k++) {
                    total = total + ohlc[j - k][4];
                }

                emaData.push([ohlc[j][0], total / dayMovingAvg]);
            } else {
                var emaPrevDay = emaData[emaData.length - 1][1];
                emaData.push([
                    ohlc[j][0],
                    (ohlc[j][4] - emaPrevDay) * multiplier + emaPrevDay
                ]);
            }
        }

        return {
            name: '' + dayMovingAvg + '-Day EMA',
            type: 'line',
            data: emaData
        };
    },
    getRsiSeries: function(ohlc, interval) {
        var rsiData = [];
        var avgGain = 0;
        var avgLoss = 0;

        for (var i = interval; i < ohlc.length; i++) {
            if (i === interval) {
                // initial day
                var totalGains = 0;
                var totalLosses = 0;

                for (var j = 1; j <= interval; j++) {
                    if (ohlc[j][4] > ohlc[j - 1][4]) {
                        totalGains = totalGains + ohlc[j][4] - ohlc[j - 1][4];
                    } else {
                        totalLosses = totalGains + ohlc[j - 1][4] - ohlc[j][4];
                    }
                }

                avgGain = totalGains / interval;
                avgLoss = totalLosses / interval;
            } else {
                // subsequent day
                if (ohlc[i][4] > ohlc[i - 1][4]) {
                    avgGain = (avgGain * (interval - 1) + ohlc[i][4] - ohlc[i - 1][4]) / interval;
                    avgLoss = (avgLoss * (interval - 1) + 0) / interval;
                } else {
                    avgGain = (avgGain * (interval - 1) + 0) / interval;
                    avgLoss = (avgLoss * (interval - 1) + ohlc[i - 1][4] - ohlc[i][4]) / interval;
                }
            }

            if (avgLoss === 0) {
                rsiData.push([
                    ohlc[i][0],
                    100
                ]);
            } else if (avgGain === 0) {
                rsiData.push([
                    ohlc[i][0],
                    0
                ]);
            } else {
                var relativeStrength = avgGain / avgLoss;

                rsiData.push([
                    ohlc[i][0],
                    100 - 100 / (1 + relativeStrength)
                ])
            }
        }

        return {
            name: '' + interval + '-Day RSI',
            type: 'line',
            data: rsiData,
            yAxis: 2
        }
    },
    /**
     * Returns the series for the Exponential Moving Average.
     **/
    getSmaSeries: function(ohlc, dayMovingAvg) {
        var smaData = [];

        for (var j = dayMovingAvg - 1; j < ohlc.length; j++) {
            var total = 0;

            for (var k = 0; k < dayMovingAvg; k++) {
                total = total + ohlc[j - k][4];
            }

            smaData.push([ohlc[j][0], total / dayMovingAvg]);
        }

        return {
            name: '' + dayMovingAvg + '-Day SMA',
            type: 'line',
            data: smaData
        };
    }
};

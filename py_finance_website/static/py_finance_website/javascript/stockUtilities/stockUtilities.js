var StockUtilities = {
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
    getSeries: function(stockSymbol, ohlc, volume, upperTechlicalIndicators) {
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

        for (var i = 0; i < upperTechlicalIndicators.length; i++) {
            if (upperTechlicalIndicators[i].indicatorType === 'SMA') {
                series.push(StockUtilities.getSmaSeries(ohlc, upperTechlicalIndicators[i].interval));
            } else if (upperTechlicalIndicators[i].indicatorType === 'EMA') {
                series.push(StockUtilities.getEmaSeries(ohlc, upperTechlicalIndicators[i].interval));
            }
        }

        return series;
    },
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

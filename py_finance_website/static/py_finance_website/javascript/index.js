$( document ).ready(function() {
    if (tradingDaysData !== undefined) {
        var upperTechnicalIndicators = [
            {
                'indicatorType': 'EMA',
                'interval': 13
            }
        ];
        var lowerTechnicalIndicators = [
            {'indicatorType': 'MACD'}
        ];
        var stockSymbol = $('#id_stockSymbol').val().toUpperCase();
        var tradingData = StockUtilities.calcOhlcVolume(tradingDaysData);
        var ohlc = tradingData.ohlc;
        var volume = tradingData.volume;

        Highcharts.stockChart('stockContainer', {
            rangeSelector: {
                selected: 1
            },
            title: {
                text: stockSymbol
            },
            yAxis: [{
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'OHLC'
                },
                height: '60%',
                lineWidth: 2
            }, {
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Volume'
                },
                top: '65%',
                height: '35%',
                offset: 0,
                lineWidth: 2
            }],
            tooltip: {
                split: true
            },
            series: StockUtilities.getSeries(stockSymbol, ohlc, volume, upperTechnicalIndicators)
        });
    }
});

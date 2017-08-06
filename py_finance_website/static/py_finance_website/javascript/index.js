$( document ).ready(function() {
    if (tradingDaysData !== undefined) {
        var upperTechnicalIndicators = [
            {
                'indicatorType': 'EMA',
                'interval': 10
            },
            {
                'indicatorType': 'EMA',
                'interval': 50
            }
        ];
        var lowerTechnicalIndicators = [
            {
                'indicatorType': 'Volume'
            },
            {
                'indicatorType': 'RSI',
                'interval': 2
            }
        ];
        var stockSymbol = $('#id_stockSymbol').val().toUpperCase();
        var tradingData = StockUtilities.calcOhlcVolume(tradingDaysData);
        var ohlc = tradingData.ohlc;
        var volume = tradingData.volume;

        Highcharts.stockChart('stockContainer', {
            plotOptions: {
                candlestick: {
                    color: 'red',
                    upColor: 'green'
                }
            },
            rangeSelector: {
                enabled: false
            },
            navigator: {
                enabled: false
            },
            scrollbar: {
                enabled: false
            },
            yAxis: [{
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'OHLC'
                },
                height: '45%',
                lineWidth: 2
            }, {
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Volume'
                },
                top: '50%',
                height: '25%',
                offset: 0,
                lineWidth: 2
            }, {
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'RSI'
                },
                top: '75%',
                height: '25%',
                offset: 0,
                lineWidth: 2
            }],
            tooltip: {
                split: true
            },
            series: StockUtilities.getSeries(stockSymbol,
                                             ohlc,
                                             volume,
                                             upperTechnicalIndicators,
                                             lowerTechnicalIndicators)
        });
    }
});

function getTestData() {
    $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=aapl-ohlcv.json&callback=?', function (data) {
        // split the data set into ohlc and volume
        console.log('test data');
        console.log(data);
        var ohlc = [],
            volume = [],
            dataLength = data.length,
            // set the allowed units for data grouping
            groupingUnits = [[
                'week',                         // unit name
                [1]                             // allowed multiples
            ], [
                'month',
                [1, 2, 3, 4, 6]
            ]],

            i = 0;

        for (i; i < dataLength; i += 1) {
            ohlc.push([
                data[i][0], // the date
                data[i][1], // open
                data[i][2], // high
                data[i][3], // low
                data[i][4] // close
            ]);

            volume.push([
                data[i][0], // the date
                data[i][5] // the volume
            ]);
        }

        print('test ohlc');
        print(ohlc);
        print(volume);


        // create the chart
        // Highcharts.stockChart('stockContainer', {
        //
        //     rangeSelector: {
        //         selected: 1
        //     },
        //
        //     title: {
        //         text: 'AAPL Historical'
        //     },
        //
        //     yAxis: [{
        //         labels: {
        //             align: 'right',
        //             x: -3
        //         },
        //         title: {
        //             text: 'OHLC'
        //         },
        //         height: '60%',
        //         lineWidth: 2
        //     }, {
        //         labels: {
        //             align: 'right',
        //             x: -3
        //         },
        //         title: {
        //             text: 'Volume'
        //         },
        //         top: '65%',
        //         height: '35%',
        //         offset: 0,
        //         lineWidth: 2
        //     }],
        //
        //     tooltip: {
        //         split: true
        //     },
        //
        //     series: [{
        //         type: 'candlestick',
        //         name: 'AAPL',
        //         data: ohlc,
        //         dataGrouping: {
        //             units: groupingUnits
        //         }
        //     }, {
        //         type: 'column',
        //         name: 'Volume',
        //         data: volume,
        //         yAxis: 1,
        //         dataGrouping: {
        //             units: groupingUnits
        //         }
        //     }]
        // });
    });
}

$( document ).ready(function() {
    if (tradingDaysData !== undefined) {
        console.log('tradingDays exists');
        console.log(tradingDaysData);
        //getTestData();
        var ohlc = [];
        var volume = [];
        var dataLength = tradingDaysData.length;
        // set the allowed units for data grouping
        var groupingUnits = [
            [
                'week',                         // unit name
                [1]                             // allowed multiples
            ],
            [
                'month',
                [1, 2, 3, 4, 6]
            ]
        ];

        for (var i = 0; i < tradingDaysData.length; i++) {
            ohlc.push([
                Date.parse(tradingDaysData[i]['Date']), // the date
                tradingDaysData[i]['Open'], // open
                tradingDaysData[i]['High'], // high
                tradingDaysData[i]['Low'], // low
                tradingDaysData[i]['Close'] // close
            ]);

            volume.push([
                Date.parse(tradingDaysData[i]['Date']), // the date
                tradingDaysData[i]['Volume'] // the volume
            ]);
        }

        console.log(ohlc);
        console.log(volume);

        Highcharts.stockChart('stockContainer', {
            rangeSelector: {
                selected: 1
            },
            title: {
                text: 'CERN Historical'
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
            series: [{
                type: 'candlestick',
                name: 'CERN',
                data: ohlc,
                dataGrouping: {
                    units: groupingUnits
                }
            }, {
                type: 'column',
                name: 'Volume',
                data: volume,
                yAxis: 1,
                dataGrouping: {
                    units: groupingUnits
                }
            }]
        });
    }
});

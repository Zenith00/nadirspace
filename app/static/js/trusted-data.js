google.load("visualization", "1", {
    packages: ["corechart", "controls"]
});
google.setOnLoadCallback(initialize);

function initialize() {
    var opts = {
        sendMethod: "auto"
    };
    var query = new google.visualization.Query('https://docs.google.com/spreadsheets/d/1huPKkJacTFqZizQ4Yd6Eo1QmfwjngWNOXnwt_0E-fBg/gviz/tq?sheet=Main', opts);
    query.setQuery("select *");
    query.send(drawChart);
}

function drawChart(response) {
    // var data = google.visualization.arrayToDataTable([
    //     ['Year', 'Sales', 'Expenses'],
    //     ['2004', 1000, 400],
    //     ['2005', 1170, 460],
    //     ['2006', 660, 1120],
    //     ['2007', 1030, 540]
    // ]);'
    var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));
    var data = response.getDataTable();

    // var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

    var columns = [];
    var series = {};
    for (var i = 0; i < data.getNumberOfColumns(); i++) {
        if (i == 0) {
            columns.push(i)
        } else {
            columns.push({
                type: data.getColumnType(i),
                label: data.getColumnLabel(i),
                calc: function (dataTable, row) {
                    return null;
                }
            });
        }

        if (i > 0) {
            series[i - 1] = {color: '#CCCCCC'};
        }
    }
    // series[data.getNumberOfColumns()] = {};
    var options = {
        'title': 'Trusteds',
        'hAxis': {
            'format': 'MM/dd'
        }, 'vAxis': {
            'title': 'Words',
            'format': 'decimal',
            'gridlines': {
                'count': -1
            }
        },
        'explorer': {},
        'focusTarget': 'category',
        'series': series

    };
    var lineChart = new google.visualization.ChartWrapper({
        'chartType': 'LineChart',
        'containerId': 'chart_div',
        'options': options
    });
    lineChart.setView({'columns': columns});
    lineChart.setOptions(options);
    var dateslider = new google.visualization.ControlWrapper({
        'controlType': 'DateRangeFilter',
        'containerId': 'filter_div',
        'options': {
            'filterColumnIndex': 0
        }
    });
    dashboard.bind(dateslider, lineChart);
    dashboard.draw(data);

    google.visualization.events.addListener(lineChart, 'select', function () {
        console.log("logged");
        var sel = lineChart.getChart().getSelection();
        console.log(sel[0]);
        // if selection length is 0, we deselected an element
        if (sel.length > 0) {
            // if row is undefined, we clicked on the legend
            if (sel[0].row === null) {
                var col = sel[0].column;
                if (columns[col] == col) {
                    columns[col] = {
                        type: data.getColumnType(col),
                        label: data.getColumnLabel(col),
                        calc: function (dataTable, row) {
                            return null;
                        }
                    };
                    console.log(data.getColumnType(col));
                    series[col - 1].color = '#CCCCCC';
                }
                else {
                    columns[col] = col;
                    series[col - 1].color = null;
                }

                lineChart.setView({'columns': columns});
                lineChart.setOptions(options);


                lineChart.draw();

            }
        }
    });

}
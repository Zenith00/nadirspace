google.load("visualization", "1", {
    packages: ["corechart", "controls"]
});
google.setOnLoadCallback(initialize);

function initialize() {
    var opts = {
        sendMethod: "auto"
    };
    var query = new google.visualization.Query('https://docs.google.com/spreadsheets/d/1huPKkJacTFqZizQ4Yd6Eo1QmfwjngWNOXnwt_0E-fBg/edit#gid=0', opts);
    query.setQuery("select *");
    query.send(drawChart);
}

function drawChart(response) {
    console.log("Rrsponse");
    // var data = google.visualization.arrayToDataTable([
    //     ['Year', 'Sales', 'Expenses'],
    //     ['2004', 1000, 400],
    //     ['2005', 1170, 460],
    //     ['2006', 660, 1120],
    //     ['2007', 1030, 540]
    // ]);'
    var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));
    var data = response.getDataTable();
    var options = {
        'title': 'Trusteds',
        'hAxis': {
            format: 'MM/dd'
        }, 'explorer': {}
    };
    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    // chart = new google.visualization.ChartWrapper();
    // chart.setDataTable(data);
    // chart.setChartType("LineChart");
    // chart.setOptions(options);
    // chart.draw(data, options);

    var columns = [];
    var series = {};
    for (var i = 0; i < data.getNumberOfColumns(); i++) {
        columns.push(i);
        if (i > 0) {
            series[i - 1] = {};
        }
    }
    // series[data.getNumberOfColumns()] = {};
    var lineChart = new google.visualization.ChartWrapper({
        'chartType': 'LineChart',
        'containerId': 'chart_div',
        'options':options
    });
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
                    // hide the data series
                    columns[col] = {
                        type: data.getColumnType(col),
                        label: data.getColumnLabel(col),
                        calc: function (dataTable, row) {
                            return null;
                        }
                    };
                    console.log(data.getColumnType(col));
                    // grey out the legend entry
                    series[col-1].color = '#CCCCCC';
                }
                else {
                    // show the data series
                    columns[col] = col;
                    series[col-1].color = null;
                }
                console.log(columns);
                console.log(series);
                var view = new google.visualization.DataView(data);
                // view.setColumns(columns);
                // chart.draw(view, options);
                // lineChart.setOption('series', series);
                lineChart.setView({'columns':columns});
                lineChart.setOptions({'series':series});
                // lineChart = new google.visualization.ChartWrapper({
                //     'chartType': 'LineChart',
                //     'containerId': 'chart_div',
                //     'dataSourceUrl':'https://docs.google.com/spreadsheets/d/1huPKkJacTFqZizQ4Yd6Eo1QmfwjngWNOXnwt_0E-fBg/edit#gid=0',
                //     'query':'select *',
                //     'options': {
                //         'width': "100vh",
                //         'height': 800
                //     }, view:{'columns':columns, 'series':series}
                // });

                lineChart.draw();

            }
        }
    });

}

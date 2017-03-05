
google.load("visualization", "1", {
    packages: ["corechart"]
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
    console.log("Rrsponse")
    // var data = google.visualization.arrayToDataTable([
    //     ['Year', 'Sales', 'Expenses'],
    //     ['2004', 1000, 400],
    //     ['2005', 1170, 460],
    //     ['2006', 660, 1120],
    //     ['2007', 1030, 540]
    // ]);'
    var data = response.getDataTable();
    var options = {
        'title': 'Trusteds',
        'hAxis': {
            format: 'MM/dd'
        }
    };
    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
    var columns = [];
    var series = {};
    for (var i = 0; i < data.getNumberOfColumns(); i++) {
        columns.push(i);
        if (i > 0) {
            series[i - 1] = {};
        }
    }


    google.visualization.events.addListener(chart, 'select', function () {
        var sel = chart.getSelection();
        // if selection length is 0, we deselected an element
        if (sel.length > 0) {
            // if row is undefined, we clicked on the legend
            if (sel[0].row === null) {
                var col = sel[0].column;
                if (columns[col] == col) {
                    // hide the data series
                    columns[col] = {
                        label: data.getColumnLabel(col),
                        type: data.getColumnType(col),
                        calc: function () {
                            return null;
                        }
                    };

                    // grey out the legend entry
                    series[col - 1].color = '#CCCCCC';
                } else {
                    // show the data series
                    columns[col] = col;
                    series[col - 1].color = null;
                }
                var view = new google.visualization.DataView(data);
                view.setColumns(columns);
                chart.draw(view, options);
            }
        }
    });

}

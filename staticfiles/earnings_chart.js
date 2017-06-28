function earnings_chart(data) {
    var earnings_canvas = document.getElementById('earnings').getContext("2d");

    var years = [];
    var stampaDataset;
    var laserDataset;
    var fresaDataset;

    $(data.categories).each(function (index, year) {
        years.push(year);
    });

    laserDataset = {
        label: "Laser",
        data: data.series[0].data,
        backgroundColor: colors[2],
        hoverBackgroundColor: colors[2],
        hoverBorderWidth: 2,
        hoverBorderColor: border_colors[2]
    };

    stampaDataset = {
        label: "Stampa3D",
        data: data.series[1].data,
        backgroundColor: colors[3],
        hoverBackgroundColor: colors[3],
        hoverBorderWidth: 2,
        hoverBorderColor: border_colors[3]
    };

    fresaDataset = {
        label: "Fresa",
        data: data.series[2].data,
        backgroundColor: colors[4],
        hoverBackgroundColor: colors[4],
        hoverBorderWidth: 2,
        hoverBorderColor: border_colors[4]
    };

    var earnings_chart = new Chart(earnings_canvas, {
            type: 'bar',
            responsive: true,

            data: {
                labels: years,
                datasets: [
                    stampaDataset,
                    laserDataset,
                    fresaDataset
                ]
            },
            options: {
                animation: {
                    duration: 10,
                },
                tooltips: {
                    mode: 'label',
                    callbacks: {
                        label: function (tooltipItem, data) {
                            return data.datasets[tooltipItem.datasetIndex].label + ": " + tooltipItem.yLabel;
                        }
                    }
                },
                scales: {
                    xAxes: [{
                        stacked: true,
                        gridLines: {display: false},
                    }],
                    yAxes: [{
                        stacked: true,
                        ticks: {
                            min: 0,
                        },
                    }],
                },
                legend: {display: true}
            }
        }
    );
}
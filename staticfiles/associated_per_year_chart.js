function draw_associated_yearly_chart(data) {
    var associated_yearly_canvas = document.getElementById('associated_yearly').getContext("2d");

    var years = [];
    var baseDataset;
    var makerDataset;

    $(data.categories).each(function (index, year) {
        years.push(year);
    });

    baseDataset = {
        label: data.series[0].name,
        data: data.series[0].data,
        backgroundColor: colors[0],
        hoverBackgroundColor: colors[0],
        hoverBorderWidth: 2,
        hoverBorderColor: border_colors[0]
    };

    makerDataset = {
        label: data.series[1].name,
        data: data.series[1].data,
        backgroundColor: colors[1],
        hoverBackgroundColor: colors[1],
        hoverBorderWidth: 2,
        hoverBorderColor: border_colors[1]
    };

    window.associated_yearly_chart = new Chart(associated_yearly_canvas, {
            type: 'bar',
            responsive: true,

            data: {
                labels: years,
                datasets: [
                    baseDataset,
                    makerDataset
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
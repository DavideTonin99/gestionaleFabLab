function draw_renewals_per_year_chart(data) {
    var renewals_per_year_canvas = document.getElementById('renewals').getContext("2d");

    var years = [];
    var renewDataset;
    var notRenewDataset;

    $(data.categories).each(function (index, year) {
        years.push(year);
    });

    renewDataset = {
        label: data.series[0].name,
        data: data.series[0].data,
        backgroundColor: colors[1],
        hoverBackgroundColor: colors[1],
        hoverBorderWidth: 2,
        hoverBorderColor: border_colors[1]
    };

    notRenewDataset = {
        label: data.series[1].name,
        data: data.series[1].data,
        backgroundColor: colors[0],
        hoverBackgroundColor: colors[0],
        hoverBorderWidth: 2,
        hoverBorderColor: border_colors[0]
    };

    window.renewals_per_year_chart = new Chart(renewals_per_year_canvas, {
            type: 'bar',
            responsive: true,

            data: {
                labels: years,
                datasets: [
                    renewDataset,
                    notRenewDataset
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
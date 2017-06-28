function association_per_month_chart(data) {
    var associated_per_month_canvas = document.getElementById('associated_per_month').getContext("2d");

    var months = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"];
    var baseDataset;
    var makerDataset;

    baseDataset = {
        label: "Base",
        data: data.series[0].data,
        backgroundColor: colors[0],
        hoverBackgroundColor: colors[0],
        hoverBorderWidth: 2,
        hoverBorderColor: border_colors[0]
    };

    makerDataset = {
        label: "Maker",
        data: data.series[1].data,
        backgroundColor: colors[1],
        hoverBackgroundColor: colors[1],
        hoverBorderWidth: 2,
        hoverBorderColor: border_colors[1]
    };

    window.associated_per_month_chart = new Chart(associated_per_month_canvas, {
            type: 'bar',
            responsive: true,

            data: {
                labels: months,
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
                            stepSize: 1,
                        },
                    }],
                },
                legend: {display: true}
            }
        }
    );
}
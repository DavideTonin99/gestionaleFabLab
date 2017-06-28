function draw_earnings_per_year_chart(data, canvas_id) {
    var earnings_canvas = document.getElementById(canvas_id).getContext("2d");

    window.earnings_per_year_chart = new Chart(earnings_canvas,
        {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [
                        data.datasets[0].data[0],
                        data.datasets[0].data[1],
                        data.datasets[0].data[2]
                    ],
                    backgroundColor: [
                        colors[0],
                        colors[1],
                        colors[2]
                    ],
                    label: 'Dataset 1'
                }],
                labels: data.labels
            },
            options: {
                responsive: true,
                legend: {
                    position: 'top',
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        }
    )
}
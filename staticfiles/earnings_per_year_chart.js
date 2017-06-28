window.earnings_per_year_chart = [undefined, undefined];

function draw_earnings_per_year_chart(data, canvas_id) {
    var earnings_canvas = document.getElementById(canvas_id).getContext("2d");

    index = 0;

    if (canvas_id === "earnings-yearly-2") index = 1;

    window.earnings_per_year_chart[index] = new Chart(earnings_canvas,
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
                        colors[2],
                        colors[3],
                        colors[4]
                    ],
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
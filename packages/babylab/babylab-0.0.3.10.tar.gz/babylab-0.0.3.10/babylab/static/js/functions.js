function colPlot(labels, values, canvas, color, label) {
  const stx = document.getElementById(canvas).getContext("2d")
  new Chart(stx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: label,
        data: values,
        backgroundColor: color,
        borderColor: color,
      }]
    },
    options: {
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: label,
          },
          grid: {
            display: false,
          },
          ticks: {
            beginAtZero: false,
            suggestedMin: 'min-int-value',
            suggestedMax: 'max-int-value'
          }
        },
        y: {
          title: {
            display: true,
            text: "# participants",
          },
          ticks: {
            beginAtZero: true,
            stepSize: 1,
            suggestedMin: 'min-int-value',
            suggestedMax: 'max-int-value'
          }
        }
      }
    }
  })
}

function circlePlot(labels, values, canvas, color, label) {
  const ttx = document.getElementById(canvas).getContext("2d")

  new Chart(ttx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "# participants",
          data: values,
        },
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
      },
      rotation: -90,
      circumference: 180,
    },
  })
}

function dateLinePlot(labels, values, canvas, color, label) {
  const ttx = document.getElementById(canvas).getContext("2d")
  new Chart(ttx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "# participants",
          data: values,
          backgroundColor: color,
          borderColor: color,
          cubicInterpolationMode: 'monotone',
          tension: 0.4,
          pointRadius: 1,
        },
      ]
    },
    options: {
      plugins: {
        legend: {
          display: true
        }
      },
      scales: {
        y: {
          title: {
            display: true,
            text: '# participants'
          },
          ticks: {
            beginAtZero: true,
            stepSize: 1,
            suggestedMin: 'min-int-value',
            suggestedMax: 'max-int-value'
          }
        },
        x: {
          type: 'time',
          time: {
            unit: "week"
          },
          title: {
            display: true,
            text: label
          }
        },
      }
    }
  })
}
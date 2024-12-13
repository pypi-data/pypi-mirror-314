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
      }]
    },
    options: {
      plugins: {
        legend: {
          display: false,
          font: {
            family: "Ciutadella Regular"
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: label,
            font: {
              family: 'Ciutadella Medium',
              size: 16
            }
          },
          grid: {
            display: false,
          },
          ticks: {
            beginAtZero: false,
            suggestedMin: 'min-int-value',
            suggestedMax: 'max-int-value',
            font: {
              family: 'Ciutadella Regular',
              size: 16
            }
          }
        },
        y: {
          title: {
            display: true,
            text: "# participants",
            font: {
              family: 'Ciutadella Medium',
              size: 16
            }
          },
          ticks: {
            beginAtZero: true,
            stepSize: 1,
            suggestedMin: 'min-int-value',
            suggestedMax: 'max-int-value',
            font: {
              family: 'Ciutadella Regular',
              size: 16
            }
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
          labels: {
            font: {
              family: 'Ciutadella Regular',
              size: 18
            }
         }
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
          display: true,
          labels: {
            font: {
              family: 'Ciutadella Regular',
              size: 18
            }
          }
        }
      },
      scales: {
        y: {
          title: {
            display: true,
            text: '# participants',
            font: {
              family: 'Ciutadella Medium',
              size: 18
            }
          },
          ticks: {
            beginAtZero: true,
            stepSize: 1,
            suggestedMin: 'min-int-value',
            suggestedMax: 'max-int-value',
            font: {
              family: 'Ciutadella Regular',
              size: 16
            }
          }
        },
        x: {
          type: 'time',
          time: {
            unit: "week"
          },
          title: {
            display: true,
            text: label,
            font: {
              family: 'Ciutadella Medium',
              size: 16
            }
          },
          ticks: {
            font: {
              family: 'Ciutadella Regular',
              size: 16
            }
          }
        },
      }
    }
  })
}
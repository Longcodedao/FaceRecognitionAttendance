var ctx = document.getElementById('pieChart').getContext('2d');
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ['In Class', 'Absent'],
    datasets: [
      {
        data: [10, 5],
        backgroundColor: ['green', 'orange'],
      },
    ],
  },
  options: {
    tooltips: {
      callbacks: {
        label: function (tooltipItem, data) {
          var label = data.labels[tooltipItem.index];
          var value = data.datasets[0].data[tooltipItem.index];
          return label + ': ' + value + '%'; // Display value as a figure
        },
      },
    },
  },
});

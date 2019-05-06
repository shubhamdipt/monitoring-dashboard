var DATA_TYPE_GRAPH_ID = {
  CPU_USAGE: "chart-cpu-",
  MEMORY_USAGE: "chart-ram-",
  DISK_SPACE_LEFT: "chart-disk-"
};
var plot_days = 7;

function format_disk_space(value) {
  return (value / 1073741824).toFixed(2)
}

function percentage_format(value) {
  return  value
}

function createGraph(device_id, device_order, data_type, data) {

  var yAxis_details = {
    labelInterpolationFnc: data_type === "DISK_SPACE_LEFT" ? format_disk_space : percentage_format
  };
  if (data_type !== "DISK_SPACE_LEFT") {
    yAxis_details["high"] = 100;
    yAxis_details["low"] = 0;
  }
  var div_element = "#" + DATA_TYPE_GRAPH_ID[data_type] + device_order;
  new Chartist.Line(div_element, {
    series: [
      {
        data: data[data_type].map(function (x) {
          return {x: new Date(x["created"]), y: x["data"]};
        })
      },
    ]
  }, {
    axisX: {
      type: Chartist.FixedScaleAxis,
      divisor: 5,
      labelInterpolationFnc: function(value) {
        return moment(value).format('MMM D HH:MM');
      }
    },
    axisY: yAxis_details
  });
}

function updateCharts(days) {
  for (var i = 0; i < devices_count; i++) {
    (function () {
      var device_id = $('input[name=device-order-'+ i +']').val();
      var device_order = i;
      $.post( "/servers/plot_server_data", {device_id: device_id, days: days},function( data ) {
        createGraph(device_id, device_order, "DISK_SPACE_LEFT", data["data"]);
        createGraph(device_id, device_order, "CPU_USAGE", data["data"]);
        createGraph(device_id, device_order, "MEMORY_USAGE", data["data"]);
      })
    })();
  }
}

function changeTimeFrame() {
  plot_days = document.getElementById("timeframe").value;
  updateCharts(plot_days);
}

$(function () {
  updateCharts(plot_days);
  setInterval(function(){updateCharts(plot_days)}, 5 * 60 * 1000);
});
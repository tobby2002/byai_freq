function splitData(rawData) {
  var categoryData = [];
  var values = [];
  for (var i = 0; i < rawData.length; i++) {
      categoryData.push(rawData[i].splice(0, 1)[0]);
      values.push(rawData[i]);
  }
  return {
      categoryData: categoryData,
      values: values
  };
}

function calculateMA(dayCount, data) {
  var result = [];
  for (var i = 0, len = data.values.length; i < len; i++) {
      if (i < dayCount) {
          result.push('-');
          continue;
      }
      var sum = 0;
      for (var j = 0; j < dayCount; j++) {
          sum += data.values[i - j][1];
      }
      result.push(sum / dayCount);
  }
  return result;
}

function calculateMA_add(dayCount, data) {
  var result = [];
  for (var i = 0, len = data.values.length; i < len; i++) {
      if (i < dayCount) {
          result.push('-');
          continue;
      }
      var sum = 0;
      for (var j = 0; j < dayCount; j++) {
          sum += data.values[i - j][1];
      }
      result.push(sum / dayCount);
  }
  return result.slice(-1)[0];
}

function getOption(t_ohlc){
  // https://echarts.baidu.com/echarts2/doc/option-en.html#title~
  // for bitcoin
  var upColor = '#00da3c';
  var upBorderColor = '#008F28';
  var downColor = '#ec0000';
  var downBorderColor = '#8A0000';

  // for stock
  // var upColor = '#ec0000';
  // var upBorderColor = '#8A0000';
  // var downColor = '#00da3c';
  // var downBorderColor = '#008F28';
  var rt = '\n'
  var option = {
    title: {
        text: 'BITMEX 1M DATA',
        left: 0
    },
    tooltip: {
        // trigger: 'axis',
        axisPointer: {
            type: 'cross'
        }
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    legend: {
        data: ['BITXBT', 'MA5', 'MA20', 'MA60']
    },
    grid: {
        left: '10%',
        right: '10%',
        bottom: '15%'
    },
    axisPointer: {
        link: {xAxisIndex: 'all'},
        label: {
            backgroundColor: '#777'
        }
    },
    xAxis: {
        type: 'category',
        data: t_ohlc.categoryData,
        scale: true,
        boundaryGap : false,
        axisLine: {onZero: false},
        axisLabel: {
            formatter: function (value) {
                return echarts.format.formatTime('yy-MM-dd' +rt+ 'hh:mm', value);
                // return echarts.format.formatTime('yy-MM-dd' +rt+ 'hh:mm:ss', value);
            }
        },
        splitLine: {show: false},
        splitNumber: 20,
        min: 'dataMin',
        max: 'dataMax'
    },
    yAxis: [
        {
            scale: true,
            position: 'right',
            splitArea: {
                show: true
            }
        }
    ],
    dataZoom: [
        {
            type: 'inside',
            realtime: true,
            start: 50,
            end: 100
        },
        {
            show: true,
            type: 'slider',
            realtime: true,
            y: '90%',
            start: 50,
            end: 100
        }
    ],
    // visualMap: {
    //     show: true,
    //     seriesIndex: 1,
    //     dimension: 6,
    //     pieces: [{
    //         value: 1,
    //         color: upColor
    //     }, {
    //         value: -1,
    //         color: downColor
    //     }]
    // },
    animation: false,
    series: [
        {
          name: 'BITXBT',
          type: 'k',
          // type: 'candlestick',
          data: t_ohlc.values,
          itemStyle: {
              normal: {
                  color: upColor,
                  color0: downColor,
                  borderColor: upBorderColor,
                  borderColor0: downBorderColor
              }
          },
          markPoint: {
              label: {
                  normal: {
                      formatter: function (param) {
                          return param != null ? Math.round(param.value) : '';
                      }
                  }
              },
              data: [
                  {
                      name: 'XX구두점',
                      coord: ['2013/5/31', 2300],
                      value: 2300,
                      itemStyle: {
                          normal: {color: 'rgb(41,60,85)'}
                      }
                  },
                  {
                      name: 'highest value',
                      type: 'max',
                      valueDim: 'highest'
                  },
                  {
                      name: 'lowest value',
                      type: 'min',
                      valueDim: 'lowest'
                  },
                  // {
                  //     name: 'average value on close',
                  //     type: 'average',
                  //     valueDim: 'close'
                  // }
              ],
              tooltip: {
                  formatter: function (param) {
                      return param.name + '<br>' + (param.data.coord || '');
                  }
              }
          },
          markLine: {
              symbol: ['none', 'none'],
              data: [
                  [
                      {
                          name: 'from lowest to highest',
                          type: 'min',
                          valueDim: 'lowest',
                          symbol: 'circle',
                          symbolSize: 10,
                          label: {
                              normal: {show: false},
                              emphasis: {show: false}
                          }
                      },
                      {
                          type: 'max',
                          valueDim: 'highest',
                          symbol: 'circle',
                          symbolSize: 10,
                          label: {
                              normal: {show: false},
                              emphasis: {show: false}
                          }
                      }
                  ],
                  {
                      name: 'min line on close',
                      type: 'min',
                      valueDim: 'close'
                  },
                  {
                      name: 'max line on close',
                      type: 'max',
                      valueDim: 'close'
                  }
              ]
          }
      },
      {
          name: 'MA5',
          type: 'line',
          data: calculateMA(5, t_ohlc),
          smooth: true,
          lineStyle: {
              normal: {opacity: 0.5}
          }
      },
      {
          name: 'MA20',
          type: 'line',
          data: calculateMA(20, t_ohlc),
          smooth: true,
          lineStyle: {
              normal: {opacity: 0.5}
          }
      },
      {
          name: 'MA60',
          type: 'line',
          data: calculateMA(60, t_ohlc),
          smooth: true,
          lineStyle: {
              normal: {opacity: 0.5}
          }
      },
    ]
  };
  return option;
}

// data = [
//   ['2013/1/24  21:10:00+00:00', 2320.26,2320.26,2287.3,2362.94],
//   ['2013/2/6', 2432.68,2434.48,2427.7,2441.73],
//   ['2013/2/28', 2322.32,2365.59,2308.92,2366.16]
// ];

var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var option = null;

function plot_chart_sh(data){
  // [datatime, open, close，low，high]
  var times_ohlcs = splitData(data);
  option = getOption(times_ohlcs);

  if (option && typeof option === "object") {
    myChart.setOption(option, true);
  }
}

// when click button
// $('#calldbtn').click(function(){

const url = 'http://127.0.0.1:8007/charts/sh';

$.ajax({
  type: "POST",
  dataType: "json",
  async: true,
  url: url,
  success: function(results){
    plot_chart_sh(results.data);
  },
  error: function(data) {
    alert(JSON.stringify(data));
  }

});

// });

function add_new_data() {
  const url = 'http://127.0.0.1:8007/charts/sh/live';
  $.ajax({
    type: "POST",
    dataType: "json",
    async: false,
    url: url,
    success: function(results){
      var t_oclh = splitData(results.data);
      // option.xAxis.data.push(['2013/1/30  21:10:00+00:00']);
      var last_time = option.xAxis.data.slice(-1)[0];
      var this_time = t_oclh.categoryData[0];

      if (this_time !== last_time) {

        // candlestick data (xAxis)
        option.xAxis.data.shift();  //remove one stick(xAxis) from all data
        option.xAxis.data.push(this_time);  //add a new stick(xAxis)

        //
        option.series[0].data.shift();
        option.series[0].data.push(t_oclh.values[0]);  // option.series[0].data.push([2360.75,2382.48,2347.89,2383.76]);

        // ma5
        option.series[1].data.shift();
        option.series[1].data.push(calculateMA_add(5, t_oclh));  // console.log('calculateMA(5, t_ohlc):' + (calculateMA_add(5, t_ohlc)).toString());
        // //
        // // // ma20
        option.series[2].data.shift();
        option.series[2].data.push(calculateMA_add(20, t_oclh));
        // //
        // // // ma60
        option.series[3].data.shift();
        option.series[3].data.push(calculateMA_add(60, t_oclh));

        myChart.setOption({
          xAxis: {
            data: option.xAxis.data
          },
          series: [{data: option.series[0].data}, {data: option.series[1].data}, {data: option.series[2].data}, {data: option.series[3].data}
          ]
        });

        // https://github.com/apache/incubator-echarts/blob/master/test/dataZoom-dynamic.html
        // https://echarts.baidu.com/echarts2/doc/doc-en.html#Line   --> find '{self} addData'  params == [[seriesIdx, data, isHead, dataGrow, additionData], [...]]
        // https://codeday.me/ko/qa/20190606/719245.html
        // myChart.addData([
        //   [
        //     0,
        //     option.series[0].data[t_ohlc.values[0]],
        //     false,
        //     false,
        //     option.xAxis.data[this_time]
        //
        //   ],
        //   [
        //     1,
        //     option.series[1].data[calculateMA(5, t_ohlc)],
        //     false,
        //     false
        //   ],
        //   [
        //     2,
        //     option.series[2].data[calculateMA(20, t_ohlc)],
        //     false,
        //     false
        //   ]
        //
        // ]);

      }

    },
    error: function(data) {
      console.log(JSON.stringify(data));
    }
  });
};
setInterval(add_new_data, 3000); // Time in milliseconds

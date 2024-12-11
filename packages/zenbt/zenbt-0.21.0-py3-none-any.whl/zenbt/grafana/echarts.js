const raw_data = context.panel.data.series[0].fields;
const position_data = context.panel.data.series[1].fields;

let date = []
let open;
let high;
let low;
let close;
let volume;
let indicators = {}
let rsi;
let atr;


for (let j = 0; j < raw_data.length; j++) {
  if (raw_data[j].name === "time") {
    raw_data[j].values.map((entry, index) => {
      date.add(new Date(entry).toLocaleString("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }) + " (" + index + ")")

    })
  } else if (raw_data[j].name === "open") {
    open = raw_data[j].values;
  } else if (raw_data[j].name === "high") {
    high = raw_data[j].values;
  } else if (raw_data[j].name === "low") {
    low = raw_data[j].values;
  } else if (raw_data[j].name === "close") {
    close = raw_data[j].values;
  } else if (raw_data[j].name === "volume") {
    volume = raw_data[j].values;
  } else if (raw_data[j].name === "rsi") {
    rsi = raw_data[j].values;
  } else if (raw_data[j].name === "atr") {
    atr = raw_data[j].values;
  } else {
    indicators[raw_data[j].name] = raw_data[j].values;
  }
}

let ohlc = [];
for (let i = 0; i < date.length; i++) {
  const openValue = open[i];
  const closeValue = close[i];
  const lowValue = low[i];
  const highValue = high[i];

  let itemStyle = {
    color: "transparent",   // Default color for bullish (rising) candlesticks
    color0: "transparent",  // Default color for bearish (falling) candlesticks
    borderColor: "gray",    // Default border color for candlesticks
    borderColor0: "gray"    // Default border color for candlesticks
  };

  if (openValue > closeValue) {
    // If the open price is higher than the close price (bearish candlestick)
    itemStyle = {
      color: "rgba(255, 0, 0, 0.5)",      // Red for bearish
      color0: "rgba(255, 0, 0, 0.5)",     // Red for bearish
      borderColor: "rgba(255, 0, 0, 0.5)", // Red border for bearish
      borderColor0: "rgba(255, 0, 0, 0.5)" // Red border for bearish
    };
  } else {
    // If the open price is lower or equal to the close price (bullish candlestick)
    itemStyle = {
      color: "rgba(0, 128, 128, 0.5)",      // Teal for bullish
      color0: "rgba(0, 128, 128, 0.5)",     // Teal for bullish
      borderColor: "rgba(0, 128, 128, 0.5)", // Teal border for bullish
      borderColor0: "rgba(0, 128, 128, 0.5)" // Teal border for bullish
    };
  }

  ohlc.push({
    value: [
      closeValue,  // close
      openValue,   // open
      lowValue,    // low
      highValue    // high
    ],
    itemStyle
  });
}




return {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    },
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    textStyle: {
      color: '#000'
    },
    // extraCssText: 'width: 170px'
  },
      axisPointer: {
        link: [
          {
            xAxisIndex: 'all'
          }
        ],
        label: {
          backgroundColor: '#777'
        }
      },
  grid: [
      {
        left: "1%",
        right: "5%",
        top: 20,
        bottom: 240,
        borderColor: "#4c4c4c",
        borderWidth: 1,
        show: true,
      },
      {
        left: "1%",
        right: "5%",
        height: 80,
        bottom: 150,
        // height: 150,
        // bottom: 60,
        borderColor: "#4c4c4c",
        borderWidth: 1,
        show: true,
      },
      {
        left: "1%",
        right: "5%",
        height: 80,
        bottom: 60,
        borderColor: "#4c4c4c",
        borderWidth: 1,
        show: true,
      },
  ],
  xAxis:  [
      {
        type: "category",
        boundaryGap: false,
        data: date,
        show: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: "dataMin",
        max: "dataMax",
      },
      {
        type: "category",
        show: false,
        gridIndex: 1,
        boundaryGap: false,
        data: date,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: "dataMin",
        max: "dataMax",
      },
      {
        type: "category",
        gridIndex: 2,
        boundaryGap: false,
        show: false,
        data: date,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: "dataMin",
        max: "dataMax",
      },

  ],
  yAxis: [
      {
        position: "right",
        scale: true,
        axisLine: { lineStyle: { color: '#ffffff' } },
        splitArea: { show: false },
        splitLine: { show: false }
      },
      {
        position: "right",
        scale: true,
        gridIndex: 1,
        splitNumber: 1,
        axisLine: { lineStyle: { color: '#ffffff' } },
        splitArea: { show: false },
        splitLine: { show: false }
      },
      {
        position: "right",
        scale: true,
        gridIndex: 2,
        splitNumber: 2,
        axisLine: { lineStyle: { color: '#ffffff' } },
        splitArea: { show: false },
        splitLine: { show: false }
      },
  ],

  dataZoom: [
    {
      type: "inside",
      xAxisIndex: [0, 1, 2],
      start: 50,
      end: 100,
    },
    {
      show: true,
      xAxisIndex: [0, 1, 2],
      type: "slider",
      bottom: 10,
      start: 10,
      end: 100,
    },
  ],
  series: [
    {
      name: 'OHLC',
      type: 'candlestick',
      data: ohlc,
    },
    {
      name: 'RSI',
      type: 'line',
      data: rsi,
      xAxisIndex: 1,
      yAxisIndex: 1,
    },
    {
      name: 'ATR',
      type: 'line',
      data: atr,
      xAxisIndex: 2,
      yAxisIndex: 2,
    }
  ]
};

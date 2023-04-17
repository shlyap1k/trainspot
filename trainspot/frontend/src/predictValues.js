import nextYear from "@/src/nextYear";
function predictValues(d) {
  const data = d.map(function(arr) {
    return arr.map(function(val) {
      if (typeof val === 'number') {
        return Number(val);
      }
      return val;
    });
  });
  const result = [['Дата','l=3', 'l=5', 'l=7']];
  const calculateForecast = (arr, l) => {
    const lastValues = arr.slice(-l); // Получаем последние l значений
    const sum = lastValues.reduce((acc, val) => acc + val, 0); // Сумма последних l значений
    return sum / l; // Прогнозное значение - среднее арифметическое
  };
  for (let i = 1; i < data.length; i++) {
    const date = nextYear(data[i][0]);
    const l3Forecast = calculateForecast(data.slice(1, i + 1).map(row => row[2]), 3);
    const l5Forecast = calculateForecast(data.slice(1, i + 1).map(row => row[3]), 5);
    const l7Forecast = calculateForecast(data.slice(1, i + 1).map(row => row[4]), 7);
    result.push([date, l3Forecast, l5Forecast, l7Forecast])
  }
  return result
}




function calculateInitialSeasonalIndices(values, periods) {
  const seasonalIndices = Array.from({ length: periods }, () => 0);

  for (let i = 0; i < values.length; i++) {
    seasonalIndices[i % periods] += values[i] / periods;
  }

  return seasonalIndices;
}

function calculateInitialTrend(values, periods) {
  const initialTrend = [];

  for (let i = periods; i < 2 * periods; i++) {
    initialTrend.push((values[i] - values[i - periods]) / periods);
  }

  return initialTrend;
}

function calculateSmoothedValue(value, trend, seasonalIndex, alpha, beta) {
  return (alpha * value) + ((1 - alpha) * (trend + seasonalIndex));
}

function calculateSeasonalIndex(value, trend, smoothedValue, seasonalIndex, gamma) {
  return (gamma * value / smoothedValue) + ((1 - gamma) * seasonalIndex);
}

export default predictValues

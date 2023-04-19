import countSeries from "@/src/statistics/utils/countSeries";

function generateSequence(y) {
  const signs = [];
  for (let i = 0; i < y.length; i++) {
    let sign;
    if (i === 0) {
      sign = y[i] < y[i + 1] ? '+' : y[i] > y[i + 1] ? '-' : y[i] > 0 ? '+' : '-';
    } else if (i === y.length - 1) {
      sign = y[i] > y[i - 1] ? '+' : y[i] < y[i - 1] ? '-' : y[i] > 0 ? '+' : '-';
    } else {
      sign = y[i] < y[i + 1] ? '+' : y[i] > y[i + 1] ? '-' : y[i] > y[i - 1] ? '+' : '-';
    }
    signs.push(sign);
  }
  return signs.join('');
}

// Модификация 2: Критерий "восходящих и нисходящих" серий
function updown_test(data) {
  data = data.slice(1).map(row => row[1])
  const n = data.length - 1
  const series = generateSequence(data)
  const counts_series = countSeries(series)
  const Vn = counts_series.plus + counts_series.minus
  const Tn = counts_series.max
  const Vkp = (1/3) * (2*n - 1) - 1.96 * Math.sqrt(((16*n)-29) / 90 )
  const Tkp = n < 26 ? 5 : n < 153 ? 6 : n < 1170 ? 7 : undefined

  return {
    name: "Критерий “восходящих” и “нисходящих” серий",
    median: null,
    series_count: Vn,
    max_series_count: Tn,
    alpha: 0.05,
    ut: 1.96,
    reject: ((Vn > Vkp) && (Tn < Tkp))
  }
}

export default updown_test

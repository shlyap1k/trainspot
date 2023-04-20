// Линейная модель
function linearRegression(data) {
  const n = data.length - 1;
  let sumX = 0;
  let sumY = 0;
  let sumXY = 0;
  let sumXX = 0;
  for (let i = 1; i <= n; i++) {
    const x = i;
    const y = data[i][1];
    sumX += x;
    sumY += y;
    sumXY += x * y;
    sumXX += x * x;
  }
  const b = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
  const a = (sumY - b * sumX) / n;
  return { a, b };
}

export default linearRegression

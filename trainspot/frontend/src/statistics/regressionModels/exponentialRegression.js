// Показательная модель
function exponentialRegression(data) {
  const n = data.length - 1;
  let sumX = 0;
  let sumY = 0;
  let sumX2Y = 0;
  let sumXYlnY = 0;
  for (let i = 1; i <= n; i++) {
    const x = i;
    const y = data[i][1];
    sumX += x;
    sumY += y;
    sumX2Y += x * x * y;
    sumXYlnY += x * y * Math.log(y);
  }
  const b = (n * sumX2Y - sumX * sumY) / (n * sumX * sumX - sumX * sumX);
  const a = Math.exp((sumY - b * sumX) / n);
  return { a, b };
}

export default exponentialRegression

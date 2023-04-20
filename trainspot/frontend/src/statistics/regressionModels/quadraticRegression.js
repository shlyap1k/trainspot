import gaussianElimination from "@/src/statistics/utils/gaussianElimination";

// Параболическая модель
function quadraticRegression(data) {
  const n = data.length - 1;
  let sumX = 0;
  let sumY = 0;
  let sumX2 = 0;
  let sumX3 = 0;
  let sumX4 = 0;
  let sumXY = 0;
  let sumX2Y = 0;
  for (let i = 1; i <= n; i++) {
    const x = i;
    const y = data[i][1];
    sumX += x;
    sumY += y;
    sumX2 += x * x;
    sumX3 += x * x * x;
    sumX4 += x * x * x * x;
    sumXY += x * y;
    sumX2Y += x * x * y;
  }
  const matrix = [
    [sumX4, sumX3, sumX2],
    [sumX3, sumX2, sumX],
    [sumX2, sumX, n],
  ];
  const vector = [sumX2Y, sumXY, sumY];
  const [a, b, c] = gaussianElimination(matrix, vector);
  return { a, b, c };
}

export default quadraticRegression

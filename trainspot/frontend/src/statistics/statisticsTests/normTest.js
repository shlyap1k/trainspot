function normTest(data) {
  const n = data.length;
  const mean = data.reduce((a, b) => a + b) / n;
  const variance = data.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / (n - 1);
  const stdDev = Math.sqrt(variance);
  const skewness = data.reduce((a, b) => a + Math.pow((b - mean) / stdDev, 3), 0) * n / ((n - 1) * (n - 2));
  const kurtosis = data.reduce((a, b) => a + Math.pow((b - mean) / stdDev, 4), 0) * (n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3)) - 3 * Math.pow((n - 1), 2) / ((n - 2) * (n - 3));
  const isNormal = Math.abs(skewness) <= 1.96 / Math.sqrt(n) && Math.abs(kurtosis - 3) <= 1.96 * Math.sqrt(24 / n);

  return {
    skewness,
    kurtosis,
    isNormal
  };
}

export default normTest

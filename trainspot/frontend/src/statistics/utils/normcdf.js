function normcdf(x) {
  const mean = 0;
  const stdDev = 1;
  const erf = (z) => {
    const t = 1 / (1 + 0.5 * Math.abs(z));
    const ans = 1 - t * Math.exp(-z*z - 1.26551223 +
                             t * (1.00002368 +
                             t * (0.37409196 +
                             t * (0.09678418 +
                             t * (-0.18628806 +
                             t * (0.27886807 +
                             t * (-1.13520398 +
                             t * (1.48851587 +
                             t * (-0.82215223 +
                             t * (0.17087277))))))))))
    return ans * (z >= 0 ? 1 : -1);
  };
  return 0.5 * (1 + erf((x - mean) / (stdDev * Math.sqrt(2))));
}

export default normcdf

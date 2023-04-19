const { erf } = require('mathjs');

function normcdf(x, mean, std) {
  const z = (x - mean) / (std * Math.sqrt(2));
  return 0.5 * (1 + erf(z));
}

export default normcdf

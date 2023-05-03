import normcdf from "@/src/statistics/utils/normcdf";

function signTest(signs) {
  const n = signs.length;
  const numPositives = signs.filter(sign => sign === '+').length;
  const numNegatives = signs.filter(sign => sign === '-').length;

  if (numPositives === numNegatives) {
    return { result: 'Не удалось принять или отвергнуть гипотезу на уровне значимости 0.05', pValue: 1 };
  }

  const T = Math.min(numPositives, numNegatives);
  const z = (T - n / 2) / Math.sqrt(n / 4);

  const pValue = 1 - normcdf(Math.abs(z));
  const result = pValue < 0.05 ? 'Гипотеза отвергается на уровне значимости 0.05' : 'Гипотеза не отвергается на уровне значимости 0.05';

  return { result, pValue };
}

export default signTest

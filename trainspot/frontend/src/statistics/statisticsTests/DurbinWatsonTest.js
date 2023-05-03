function DurbinWatsonTest(data) {
  const n = data.length;
  let diffSum = 0;
  for (let i = 1; i < n; i++) {
    const diff = data[i] - data[i - 1];
    diffSum += diff ** 2;
  }
  const d = diffSum / (data.reduce((sum, value) => sum + value ** 2, 0));

  if (d > 2) {
    return "Подозрение на отрицательную автокорреляцию";
  } else if (d < 2) {
    return "Подозрение на положительную автокорреляцию";
  } else {
    return "Нет оснований отвергать гипотезу о независимости значений остатков между собой";
  }
}

export default DurbinWatsonTest

// Гауссова эллиминация для решения системы линейных уравнений
function gaussianElimination(matrix, vector) {
  const n = vector.length;
  const a = matrix.map((row) => [...row]);
  const b = [...vector];
  for (let i = 0; i < n; i++) {
    // Поиск максимального элемента в столбце
    let max = Math.abs(a[i][i]);
    let maxRow = i;
    for (let j = i + 1; j < n; j++) {
      if (Math.abs(a[j][i]) > max) {
        max = Math.abs(a[j][i]);
        maxRow = j;
      }
    }
    // Перестановка строк
    for (let k = i; k < n; k++) {
      const temp = a[i][k];
      a[i][k] = a[maxRow][k];
      a[maxRow][k] = temp;
    }
    const temp = b[i];
    b[i] = b[maxRow];
    b[maxRow] = temp;
    // Прямой ход
    for (let j = i + 1; j < n; j++) {
      const c = -a[j][i] / a[i][i];
      for (let k = i + 1; k < n; k++) {
        a[j][k] += c * a[i][k];
      }
      b[j] += c * b[i];
      a[j][i] = 0;
    }
  }
  // Обратный ход
  const x = new Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) {
    let sum = 0;
    for (let j = i + 1; j < n; j++) {
      sum += a[i][j] * x[j];
    }
    x[i] = (b[i] - sum) / a[i][i];
  }
  return x;
}

export default gaussianElimination

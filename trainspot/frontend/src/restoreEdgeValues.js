function restoreEdgeValues(data) {
  let l3 = getColumnFromArray(data.slice(1), 2)
  let l5 = getColumnFromArray(data.slice(1), 3)
  let l7 = getColumnFromArray(data.slice(1), 4)

  let avgIncL3 = calculateAverageAbsoluteIncrement(l3)
  let avgIncL5 = calculateAverageAbsoluteIncrement(l5)
  let avgIncL7 = calculateAverageAbsoluteIncrement(l7)

  let restoredL3 = restoreNullValuesFromEnd(l3, avgIncL3)
  restoredL3 = restoreNullValuesFromBegin(restoredL3, avgIncL3)

  let restoredL5 = restoreNullValuesFromEnd(l5, avgIncL5)
  restoredL5 = restoreNullValuesFromBegin(restoredL5, avgIncL5)

  let restoredL7 = restoreNullValuesFromEnd(l7, avgIncL7)
  restoredL7 = restoreNullValuesFromBegin(restoredL7, avgIncL7)

  for(let i = 1; i < data.length; i++) {
    data[i][2] = restoredL3[i-1]
    data[i][3] = restoredL5[i-1]
    data[i][4] = restoredL7[i-1]
  }
  return data
}
function getColumnFromArray(arr, columnIndex) {
  const columnArray = [];
  for (let i = 0; i < arr.length; i++) {
    columnArray.push(arr[i][columnIndex]);
  }
  return columnArray;
}
function restoreNullValuesFromBegin(arr, averageAbsoluteIncrement) {
  let firstIndex = 0;
  let nullCount = 0;
  let firstNonNullValue = null;

  // Определяем индекс, с которого начинается последовательность null в начале массива
  while (firstIndex < arr.length && arr[firstIndex] === null) {
    firstIndex++;
    nullCount++;
  }

  if (nullCount === 0) {
    // Если в массиве нет null значений в начале, возвращаем исходный массив
    return arr;
  }

  if (firstIndex < arr.length) {
    // Запоминаем первое ненулевое значение
    firstNonNullValue = arr[firstIndex];
  }

  // Вычисляем значение, которое нужно добавить к первому ненулевому значению
  const increment = averageAbsoluteIncrement * nullCount;

  // Заменяем значения null в начале массива
  while (nullCount > 0) {
    arr[firstIndex - 1] = arr[firstIndex] - increment;
    firstIndex--;
    nullCount--;
  }

  return arr;
}
function restoreNullValuesFromEnd(arr, averageAbsoluteIncrement) {
  let lastIndex = arr.length - 1;
  let nullCount = 0;
  let lastNonNullValue = null;

  // Определяем индекс, с которого начинается последовательность null в конце массива
  while (lastIndex >= 0 && arr[lastIndex] === null) {
    lastIndex--;
    nullCount++;
  }

  if (nullCount === 0) {
    // Если в массиве нет null значений в конце, возвращаем исходный массив
    return arr;
  }

  if (lastIndex >= 0) {
    // Запоминаем последнее ненулевое значение
    lastNonNullValue = arr[lastIndex];
  }

  // Вычисляем значение, которое нужно добавить к последнему ненулевому значению
  const increment = averageAbsoluteIncrement * nullCount;

  // Заменяем значения null в конце массива
  while (nullCount > 0) {
    arr[lastIndex + 1] = arr[lastIndex] + increment;
    lastIndex++;
    nullCount--;
  }

  return arr;
}

function calculateAverageAbsoluteIncrement(arr) {
  let sumDiff = 0; // Сумма абсолютных приростов
  let count = 0; // Количество активных участков

  for (let i = 1; i < arr.length - 1; i++) {
    if (arr[i] !== null) {
      // Если текущий элемент не равен null и хотя бы один из соседних элементов не равен null
      sumDiff += Math.abs(arr[i] - arr[i - 1]);
      count++;
    }
  }

  if (count === 0) {
    // Если не найдено активных участков, возвращаем 0
    return 0;
  }

  // Вычисляем средний абсолютный прирост
  return sumDiff / count;
}

export default restoreEdgeValues

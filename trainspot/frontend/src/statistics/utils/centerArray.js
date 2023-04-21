function centerArray(arr) {
  let startCount = 0; // количество null в начале массива
  let endCount = 0; // количество null в конце массива

  // Проверяем наличие null в массиве
  if (!arr.includes(null)) {
    return arr;
  }

  // Подсчитываем количество null в начале массива
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === null) {
      startCount++;
    } else {
      break; // выходим из цикла, если находим первый не null элемент
    }
  }

  // Подсчитываем количество null в конце массива
  for (let i = arr.length - 1; i >= 0; i--) {
    if (arr[i] === null) {
      endCount++;
    } else {
      break; // выходим из цикла, если находим первый не null элемент
    }
  }

  // Если количество null в начале и в конце массива уже равно или разница между ними не превышает 1, возвращаем исходный массив
  if (startCount === endCount || Math.abs(startCount - endCount) <= 1) {
    return arr;
  }

  // Если количество null в начале больше, выкидываем null из начала и вставляем их в конец массива
  if (startCount > endCount) {
    while (startCount > endCount + 1) {
      arr.push(null); // добавляем null в конец массива
      arr.shift(); // удаляем null из начала массива
      startCount--;
      endCount++;
    }
  }
  // Если количество null в конце больше, выкидываем null из конца и вставляем их в начало массива
  else {
    while (endCount > startCount + 1) {
      arr.unshift(null); // добавляем null в начало массива
      arr.pop(); // удаляем null из конца массива
      endCount--;
      startCount++;
    }
  }

  // Возвращаем выровненный массив
  return arr;
}

export default centerArray

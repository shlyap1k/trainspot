function countSeries(str) {
  let countPlus = 0;
  let countMinus = 0;
  let currentChar = '';
  let currentCount = 0;
  let maxCount = 0;

  for (let i = 0; i < str.length; i++) {
    if (str[i] !== currentChar) {
      if (currentChar === '+') {
        countPlus++;
      } else if (currentChar === '-') {
        countMinus++;
      }

      if (currentCount > maxCount) {
        maxCount = currentCount;
      }

      currentChar = str[i];
      currentCount = 1;
    } else {
      currentCount++;
    }
  }

  if (currentChar === '+') {
    countPlus++;
  } else if (currentChar === '-') {
    countMinus++;
  }

  if (currentCount > maxCount) {
    maxCount = currentCount;
  }

  return {
    plus: countPlus,
    minus: countMinus,
    max: maxCount
  };
}

export default countSeries

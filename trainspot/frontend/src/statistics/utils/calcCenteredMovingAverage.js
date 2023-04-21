function myCalculateCenteredMovingAverage(data, windowSize) {
  const result = [];
  for (let k = 0; k < data.length; k++) {
    result[k] = null
  }
  const dataLength = data.length;
  let index = 0;
  for (let i = Math.floor(windowSize / 2); i < dataLength - Math.floor(windowSize / 2); i++) {
    let sum = 0;
    for (let j = i - Math.floor(windowSize / 2); j <= i + Math.floor(windowSize / 2); j++) {
      // console.log(data[j].isArray)

      sum += data[j][1];
      index = j
    }
    result[index-1] = sum / windowSize;
  }
  return result;
}

export default myCalculateCenteredMovingAverage

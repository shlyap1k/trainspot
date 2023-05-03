function chooseBestModel(models) {
  let bestModel = null;
  let maxCount = -1;

  for (const modelKey of Object.keys(models)) {
    let count = 0;
    for (const key of Object.keys(models[Object.keys(models)[0]])) {
      const values = Object.values(models).map((m) => m[key]);
      const minValue = Math.min(...values);
      if (models[modelKey][key] === minValue) {
        count++;
      }
    }
    if (count > maxCount) {
      maxCount = count;
      bestModel = modelKey;
    }
  }
  const names = {linear: 'Линейная', quadratic: 'Параболическая', exponential: 'Показательная'}

  return names[bestModel];
}

export default chooseBestModel

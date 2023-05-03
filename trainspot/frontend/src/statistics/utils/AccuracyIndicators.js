function calcAccuracyIndicators(actuals, predicted) {
  return {
    MAPE: calcMAPE(actuals, predicted),
    S: calcS(actuals, predicted),
    SSE: calcSSE(actuals, predicted),
    MSE: calcMSE(actuals, predicted)
  }
}

// Вычисление MAPE
function calcMAPE(actuals, predicted) {
  const absPercErrors = actuals.map((actual, i) => Math.abs(actual - predicted[i]) / actual * 100);
  return absPercErrors.reduce((sum, error) => sum + error, 0) / actuals.length;
}

// Вычисление S
function calcS(actuals, predicted) {
  const squaredErrors = actuals.map((actual, i) => (actual - predicted[i]) ** 2);
  return Math.sqrt(squaredErrors.reduce((sum, error) => sum + error, 0) / (actuals.length - 1));
}

// Вычисление SSE
function calcSSE(actuals, predicted) {
  const squaredErrors = actuals.map((actual, i) => (actual - predicted[i]) ** 2);
  return squaredErrors.reduce((sum, error) => sum + error, 0);
}

// Вычисление MSE
function calcMSE(actuals, predicted) {
  const squaredErrors = actuals.map((actual, i) => (actual - predicted[i]) ** 2);
  return squaredErrors.reduce((sum, error) => sum + error, 0) / actuals.length;
}

export default calcAccuracyIndicators

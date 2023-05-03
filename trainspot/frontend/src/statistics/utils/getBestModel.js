function chooseBestModel(models) {
  let bestModel = null;
  let minMAPE = Infinity;
  let minS = Infinity;
  let minSSE = Infinity;
  let minMSE = Infinity;
  let maxParams = -1;

  for (let model in models) {
    const { MAPE, S, SSE, MSE, params } = models[model];
    if (MAPE < minMAPE) {
      bestModel = model;
      minMAPE = MAPE;
      minS = S;
      minSSE = SSE;
      minMSE = MSE;
      maxParams = params;
    } else if (MAPE === minMAPE) {
      if (S < minS) {
        bestModel = model;
        minS = S;
        minSSE = SSE;
        minMSE = MSE;
        maxParams = params;
      } else if (S === minS) {
        if (SSE < minSSE) {
          bestModel = model;
          minSSE = SSE;
          minMSE = MSE;
          maxParams = params;
        } else if (SSE === minSSE) {
          if (MSE < minMSE) {
            bestModel = model;
            minMSE = MSE;
            maxParams = params;
          } else if (MSE === minMSE) {
            if (params > maxParams) {
              bestModel = model;
              maxParams = params;
            }
          }
        }
      }
    }
  }

  return bestModel;
}

export default chooseBestModel

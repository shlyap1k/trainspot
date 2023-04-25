// Модификация 1: Критерий серий, основанный на медиане выборки
// import normcdf from "@/src/statistics/normcdf";
import {median} from "mathjs";
import countSeries from "@/src/statistics/utils/countSeries";


function median_test(yt) {
  yt = yt.slice(1).map(row => row[1])
  const alpha = 0.05; // Уровень значимости
  const ut = 1.96; // Квантиль нормального распределения уровня (1-alpha)/2

  // Шаг 1: построение вариационного ряда
  const rankedYt = yt.slice().sort((a, b) => a - b);

  // Шаг 2: нахождение медианы вариационного ряда
  const n = rankedYt.length;
  const median = n % 2 === 0 ? (rankedYt[n / 2 - 1] + rankedYt[n / 2]) / 2 : rankedYt[Math.floor(n / 2)];
  // Шаг 3: создание последовательности "+" и "-"
  const signs = yt.map(y => {
    if (y > median) {
      return "+";
    } else if (y < median) {
      return "-";
    } else {
      return "";
    }
  }).join("");

  // Шаг 4: нахождение количества серий и длины самой длинной серии
  const series = countSeries(signs);
  const v = series.plus + series.minus;
  const t = series.max;

  // Шаг 5: проверка гипотезы
  const u = ut * Math.sqrt((v - 1) / 2);
  const w = ut * Math.sqrt((v + 1) / (6 * n));
  const isRandom = t <= u && v > w;

  // Вывод результата
  // console.log("median", median)
  // console.log("Количество серий (округлено вниз до ближайшего целого):", v);
  // console.log("Длина самой длинной серии (округлено вниз до ближайшего целого):", t);
  // console.log("Уровень значимости (alpha):", alpha);
  // console.log("Квантиль нормального распределения (ut):", ut);
  // console.log("Гипотеза об отсутствии тренда:", isRandom ? "принимается" : "отвергается");
  return {
    name: "Критерий серий, основанный на медиане выборки",
    median: median,
    series_count: v,
    max_series_count: t,
    alpha: alpha,
    ut: ut,
    reject: isRandom,
    signs: signs
  }
}

export default median_test

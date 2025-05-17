
import { SimulationResult } from "@/types/simulation";

export const mockSimulationResults: SimulationResult[] = [
  {
    year: 0,
    age: 26,
    income: 20,
    postTaxIncome: 14,
    expenditure: 4,
    savingsThisYear: 10,
    totalSavings: 20,
    totalDebt: 0,
    events: "Initial State"
  },
  {
    year: 1,
    age: 27,
    income: 21.5,
    postTaxIncome: 15.05,
    expenditure: 4.28,
    savingsThisYear: 10.77,
    totalSavings: 31.77,
    totalDebt: 0,
    events: "Normal Year"
  },
  {
    year: 2,
    age: 28,
    income: 23.7,
    postTaxIncome: 16.59,
    expenditure: 4.58,
    savingsThisYear: 12.01,
    totalSavings: 45.94,
    totalDebt: 0,
    events: "💒 Child 1 Marriage (-30.00L, Age 25)"
  },
  {
    year: 3,
    age: 29,
    income: 25.1,
    postTaxIncome: 17.57,
    expenditure: 4.9,
    savingsThisYear: 12.67,
    totalSavings: 59.94,
    totalDebt: 0,
    events: "Normal Year"
  },
  {
    year: 4,
    age: 30,
    income: 26.9,
    postTaxIncome: 18.83,
    expenditure: 5.24,
    savingsThisYear: 13.59,
    totalSavings: 75.91,
    totalDebt: 0,
    events: "🧨 Job Loss Started (6 months)"
  },
  {
    year: 5,
    age: 31,
    income: 0,
    postTaxIncome: 0,
    expenditure: 5.61,
    savingsThisYear: -5.61,
    totalSavings: 70.7,
    totalDebt: 0,
    events: "🧨 Job Loss Ongoing (0 yrs left), 💸 Job Ended. New salary 16.14L. Recovery: 2 yrs."
  },
  {
    year: 6,
    age: 32,
    income: 21.52,
    postTaxIncome: 15.06,
    expenditure: 6,
    savingsThisYear: 9.06,
    totalSavings: 81.43,
    totalDebt: 0,
    events: "📈 Job Recovery. Income: 21.52L. 1 yrs left., 👶 Child 1 Born (-3.50L)"
  },
  {
    year: 7,
    age: 33,
    income: 26.9,
    postTaxIncome: 18.83,
    expenditure: 6.66,
    savingsThisYear: 12.17,
    totalSavings: 96.74,
    totalDebt: 0,
    events: "📈 Job Recovery. Income: 26.90L. 0 yrs left."
  },
  {
    year: 8,
    age: 34,
    income: 28.78,
    postTaxIncome: 20.15,
    expenditure: 7.39,
    savingsThisYear: 12.76,
    totalSavings: 112.98,
    totalDebt: 0,
    events: "Normal Year"
  },
  {
    year: 9,
    age: 35,
    income: 30.8,
    postTaxIncome: 21.56,
    expenditure: 8.2,
    savingsThisYear: 13.36,
    totalSavings: 130.24,
    totalDebt: 0,
    events: "👨‍👩‍👧‍👦 Family Expense (-10.50L)"
  },
  {
    year: 10,
    age: 36,
    income: 33,
    postTaxIncome: 23.1,
    expenditure: 8.77,
    savingsThisYear: 14.33,
    totalSavings: 149.26,
    totalDebt: 0,
    events: "🚀 Career Advancement! New Income: 35.64L (Age 36)"
  },
  {
    year: 11,
    age: 37,
    income: 35.64,
    postTaxIncome: 24.95,
    expenditure: 9.39,
    savingsThisYear: 15.56,
    totalSavings: 170.45,
    totalDebt: 0,
    events: "Normal Year"
  },
  {
    year: 12,
    age: 38,
    income: 38.13,
    postTaxIncome: 26.69,
    expenditure: 10.04,
    savingsThisYear: 16.65,
    totalSavings: 193.65,
    totalDebt: 0,
    events: "Normal Year"
  },
  {
    year: 13,
    age: 39,
    income: 40.8,
    postTaxIncome: 28.56,
    expenditure: 10.75,
    savingsThisYear: 17.81,
    totalSavings: 218.83,
    totalDebt: 0,
    events: "📉 Market Crash! Equity returns -25%. Recovery: 3 yrs."
  },
  {
    year: 14,
    age: 40,
    income: 43.66,
    postTaxIncome: 30.56,
    expenditure: 11.5,
    savingsThisYear: 19.06,
    totalSavings: 230.42,
    totalDebt: 0,
    events: "📉 Market Recovery Ongoing (2 yrs left)"
  },
  {
    year: 15,
    age: 41,
    income: 46.71,
    postTaxIncome: 32.7,
    expenditure: 12.31,
    savingsThisYear: 20.39,
    totalSavings: 253.38,
    totalDebt: 0,
    events: "📉 Market Recovery Ongoing (1 yrs left), 🏥 Medical Emergency (-15.20L)"
  },
];

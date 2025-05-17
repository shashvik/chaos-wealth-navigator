
export interface SimulationParams {
  initialIncome: number;
  initialExpenditure: number;
  initialCapital: number;
  currentAge: number;
  futureAge: number;
  luckFactor: "unlucky" | "neutral" | "lucky";
}

export interface SimulationResult {
  year: number;
  age: number;
  income: number;
  postTaxIncome: number;
  expenditure: number;
  savingsThisYear: number;
  totalSavings: number;
  totalDebt: number;
  events: string;
}

export interface SimulationSummary {
  totalGrowthPercentage: number;
  finalSavings: number;
  highestSavings: number;
  lowestSavings: number;
  yearsInDebt: number;
  maxDebt: number;
  totalEvents: number;
}

export const getSimulationSummary = (results: SimulationResult[]): SimulationSummary => {
  if (!results.length) return {
    totalGrowthPercentage: 0,
    finalSavings: 0,
    highestSavings: 0,
    lowestSavings: 0,
    yearsInDebt: 0,
    maxDebt: 0,
    totalEvents: 0
  };

  const initialSavings = results[0].totalSavings;
  const finalSavings = results[results.length - 1].totalSavings;
  
  const savingsValues = results.map(r => r.totalSavings);
  const highestSavings = Math.max(...savingsValues);
  const lowestSavings = Math.min(...savingsValues);
  
  const yearsInDebt = results.filter(r => r.totalDebt > 0).length;
  const debtValues = results.map(r => r.totalDebt);
  const maxDebt = Math.max(...debtValues);
  
  const totalEvents = results.filter(r => r.events !== "Normal Year").length;
  
  // Calculate growth percentage
  const totalGrowthPercentage = initialSavings === 0 
    ? (finalSavings > 0 ? 100 : 0) 
    : ((finalSavings - initialSavings) / initialSavings) * 100;

  return {
    totalGrowthPercentage,
    finalSavings,
    highestSavings,
    lowestSavings,
    yearsInDebt,
    maxDebt,
    totalEvents
  };
};

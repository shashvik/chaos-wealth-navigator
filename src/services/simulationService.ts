
import { SimulationParams, SimulationResult } from "@/types/simulation";
import { mockSimulationResults } from "@/data/mockSimulation";

export const runSimulation = async (params: SimulationParams): Promise<SimulationResult[]> => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  // For demo purposes, generate a more dynamic and complete dataset based on input parameters
  const yearCount = params.futureAge - params.currentAge;
  const baseResults = mockSimulationResults.slice(0, yearCount + 1);
  
  // Scale initial values based on user inputs
  const incomeMultiplier = params.initialIncome / 20;
  const expenditureMultiplier = params.initialExpenditure / 4;
  const capitalMultiplier = params.initialCapital / 20;
  
  // Create new array with modified data, maintaining events
  return baseResults.map((result, index) => {
    // Adjust age and year based on user inputs
    const age = params.currentAge + index;
    const year = new Date().getFullYear() + index;
    
    // Scale financial data based on user inputs while preserving growth patterns
    const income = result.income * incomeMultiplier;
    const postTaxIncome = result.postTaxIncome * incomeMultiplier;
    const expenditure = result.expenditure * expenditureMultiplier;
    
    // Calculate savings with the new values
    const savingsThisYear = postTaxIncome - expenditure;
    
    // Scale total savings while preserving growth/decline patterns
    const totalSavings = result.totalSavings * capitalMultiplier;
    
    // Adjust debt levels based on initial capital ratio
    const totalDebt = result.totalDebt * (params.initialCapital > 10 ? 0.8 : 1.2);
    
    return {
      ...result,
      year,
      age,
      income,
      postTaxIncome,
      expenditure,
      savingsThisYear,
      totalSavings,
      totalDebt
    };
  });
};

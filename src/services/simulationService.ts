
import { SimulationParams, SimulationResult } from "@/types/simulation";
import { mockSimulationResults } from "@/data/mockSimulation";

// In a real app, this would be a call to your Python backend
export const runSimulation = async (params: SimulationParams): Promise<SimulationResult[]> => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  // In a production app, we'd make an actual API call here
  // return await fetch('/api/simulate', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(params)
  // }).then(res => res.json());
  
  // For demo purposes, return mock data with some randomization
  return mockSimulationResults.map(result => ({
    ...result,
    income: result.income * (params.initialIncome / 20),
    expenditure: result.expenditure * (params.initialExpenditure / 4),
    totalSavings: result.totalSavings * (params.initialCapital / 20)
  }));
};

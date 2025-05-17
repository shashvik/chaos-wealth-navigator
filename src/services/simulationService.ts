
import { SimulationParams, SimulationResult } from "@/types/simulation";

const API_URL = 'http://localhost:5001/simulate'; // Backend API URL

export const runSimulation = async (params: SimulationParams): Promise<SimulationResult[]> => {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    });

    if (!response.ok) {
      // Try to parse error message from backend if available
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorMessage;
      } catch (e) {
        // If parsing error response fails, use the default HTTP error
        console.warn("Could not parse error response from API", e);
      }
      throw new Error(errorMessage);
    }

    const results: SimulationResult[] = await response.json();
    return results;
  } catch (error) {
    console.error("Error calling simulation API:", error);
    // Rethrow the error so it can be caught by the UI layer and displayed to the user
    throw error;
  }
};

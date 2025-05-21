import { type SensitivityParams, type SuccessfulCombination } from '@/pages/SensitivityAnalysis'; // Adjust path as needed

const API_BASE_URL = import.meta.env.VITE_API_URL || '/'; // Fallback to relative path for Vercel

async function runAnalysis(params: SensitivityParams): Promise<SuccessfulCombination[]> {
  try {
    const response = await fetch(`${API_BASE_URL}sensitivity_analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Failed to parse error response' }));
      console.error('API Error:', response.status, errorData);
      throw new Error(`API request failed with status ${response.status}: ${errorData.message || response.statusText}`);
    }

    const data: SuccessfulCombination[] = await response.json();
    return data;
  } catch (error) {
    console.error('Error running sensitivity analysis:', error);
    throw error; // Re-throw to be caught by the component
  }
}

export const sensitivityAnalysisService = {
  runAnalysis,
};
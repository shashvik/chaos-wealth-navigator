import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { sensitivityAnalysisService } from '@/services/sensitivityAnalysisService';

interface SensitivityParams {
  income_min: number;
  income_max: number;
  income_step: number;
  expenditure_min: number;
  expenditure_max: number;
  expenditure_step: number;
  capital_min: number;
  capital_max: number;
  capital_step: number;
  current_age: number;
  future_age: number;
  luck_factor: string;
  num_simulations_per_combination: number;
  success_threshold_savings: number;
  min_success_rate_pct: number;
}

interface SuccessfulCombination {
  initial_income: number;
  initial_expenditure: number;
  initial_capital: number;
  success_rate_pct: number;
  average_final_savings: number;
  median_final_savings: number;
  num_successful_runs: number;
  num_total_runs: number;
}

const SensitivityAnalysisPage: React.FC = () => {
  const [params, setParams] = useState<SensitivityParams>({
    income_min: 10,
    income_max: 30,
    income_step: 5,
    expenditure_min: 2,
    expenditure_max: 8,
    expenditure_step: 1,
    capital_min: 5,
    capital_max: 40,
    capital_step: 5,
    current_age: 26,
    future_age: 60,
    luck_factor: 'neutral',
    num_simulations_per_combination: 10, // Lower for faster testing, increase for accuracy
    success_threshold_savings: 200, // 2 Crore
    min_success_rate_pct: 50,
  });
  const [results, setResults] = useState<SuccessfulCombination[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setParams(prev => ({ ...prev, [name]: name === 'luck_factor' ? value : parseFloat(value) }));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setError(null);
    setResults([]);
    try {
      const response = await sensitivityAnalysisService.runAnalysis(params);
      setResults(response);
    } catch (err) {
      setError('Failed to run sensitivity analysis. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Sensitivity Analysis Parameters</CardTitle>
          <CardDescription>Define the ranges for financial parameters to analyze.</CardDescription>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.keys(params).map(key => (
            <div key={key} className="space-y-1">
              <Label htmlFor={key} className="capitalize">{key.replace(/_/g, ' ')}</Label>
              {key === 'luck_factor' ? (
                <select 
                  id={key} 
                  name={key} 
                  value={params[key as keyof SensitivityParams]} 
                  onChange={handleChange} 
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="neutral">Neutral</option>
                  <option value="lucky">Lucky</option>
                  <option value="unlucky">Unlucky</option>
                </select>
              ) : (
                <Input 
                  id={key} 
                  name={key} 
                  type="number" 
                  value={params[key as keyof SensitivityParams]} 
                  onChange={handleChange} 
                  step={key.includes('_step') ? 0.1 : 1}
                />
              )}
            </div>
          ))}
        </CardContent>
        <CardFooter>
          <Button onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? 'Analyzing...' : 'Run Analysis'}
          </Button>
        </CardFooter>
      </Card>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Successful Combinations</CardTitle>
            <CardDescription>Parameter sets that met the success criteria.</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Income</TableHead>
                  <TableHead>Expenditure</TableHead>
                  <TableHead>Capital</TableHead>
                  <TableHead>Success Rate (%)</TableHead>
                  <TableHead>Avg. Final Savings</TableHead>
                  <TableHead>Median Final Savings</TableHead>
                  <TableHead>Successful Runs</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((res, index) => (
                  <TableRow key={index}>
                    <TableCell>{res.initial_income}L</TableCell>
                    <TableCell>{res.initial_expenditure}L</TableCell>
                    <TableCell>{res.initial_capital}L</TableCell>
                    <TableCell>{res.success_rate_pct.toFixed(2)}%</TableCell>
                    <TableCell>{res.average_final_savings.toFixed(2)}L</TableCell>
                    <TableCell>{res.median_final_savings.toFixed(2)}L</TableCell>
                    <TableCell>{res.num_successful_runs}/{res.num_total_runs}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SensitivityAnalysisPage;
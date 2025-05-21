import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

interface AnalysisResult {
  initial_income: number;
  initial_expenditure_calculated: number;
  initial_capital: number;
  success_rate_pct: number;
  average_final_savings: number;
  median_final_savings: number;
  num_successful_runs: number;
  num_total_runs: number;
  average_debt_incurred_years: number;
}

interface DebtTippingPointChartProps {
  data: AnalysisResult[];
}

const DebtTippingPointChart: React.FC<DebtTippingPointChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return <p>No data available to display the debt tipping point chart.</p>;
  }

  // Group data by initial_capital, then by initial_income
  const processedData: { name: string; [key: string]: number | string }[] = [];
  const capitalLevels = Array.from(new Set(data.map(item => item.initial_capital))).sort((a, b) => a - b);
  const incomeLevels = Array.from(new Set(data.map(item => item.initial_income))).sort((a, b) => a - b);

  incomeLevels.forEach(income => {
    const entry: { name: string; [key: string]: number | string } = { name: `Income ${income}L` };
    capitalLevels.forEach(capital => {
      const item = data.find(d => d.initial_income === income && d.initial_capital === capital);
      entry[`Capital ${capital}L`] = item ? item.average_debt_incurred_years : 0;
    });
    processedData.push(entry);
  });

  // Define colors for bars - can be expanded or made dynamic
  const barColors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#d0ed57', '#a4de6c', '#8dd1e1', '#83a6ed', '#8a8a8a', '#a0a0a0'];

  return (
    <Card className="mt-8">
      <CardHeader>
        <CardTitle>Debt Incurrence Analysis</CardTitle>
        <CardDescription>
          Average number of years debt is incurred based on initial income and capital.
          Lower values are better, indicating fewer years in debt.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={500}>
          <BarChart data={processedData} margin={{ top: 20, right: 30, left: 20, bottom: 70 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" angle={-45} textAnchor="end" interval={0} height={100}>
              <Label value="Initial Income Level" offset={30} position="insideBottom" />
            </XAxis>
            <YAxis>
              <Label value="Avg. Years Debt Incurred" angle={-90} position="insideLeft" style={{ textAnchor: 'middle' }} />
            </YAxis>
            <Tooltip formatter={(value: number) => `${value.toFixed(2)} years`} />
            <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: '20px' }} />
            {capitalLevels.map((capital, index) => (
              <Bar key={`capital-${capital}`} dataKey={`Capital ${capital}L`} fill={barColors[index % barColors.length]} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default DebtTippingPointChart;
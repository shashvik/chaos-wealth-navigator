import React from 'react';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

interface ChartDataPoint {
  initial_income: number;
  initial_capital: number;
  average_debt_occurrences: number;
  // Add other relevant fields if needed for tooltips or coloring
  success_rate_pct: number;
}

interface DebtTippingPointChartProps {
  data: ChartDataPoint[];
}

const DebtTippingPointChart: React.FC<DebtTippingPointChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return <p>No data available to display the chart.</p>;
  }

  // Prepare data for a 2D scatter plot: Debt Occurrences vs. Income, colored by Capital
  // Or, use a 3D-like approach if suitable (Recharts primarily supports 2D with ZAxis for bubble size/color)
  // For simplicity, let's do Debt vs Income, and use Capital for color or size if possible, or create facets.

  // Example: Scatter plot of Debt Occurrences vs. Income
  // We can create multiple series for different capital levels if that makes sense
  // Or use ZAxis for bubble size representing capital, if that's visually effective.

  // Let's try a simple scatter plot: X = Income, Y = Avg Debt Occurrences, Z (bubble size) = Capital
  const chartData = data.map(item => ({
    x: item.initial_income,
    y: item.average_debt_occurrences,
    z: item.initial_capital, // Capital will determine bubble size
    success_rate: item.success_rate_pct
  }));

  return (
    <div style={{ width: '100%', height: 400 }} className="my-8">
      <h3 className="text-lg font-semibold mb-4">Debt Occurrences vs. Income & Capital</h3>
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart
          margin={{
            top: 20,
            right: 20,
            bottom: 20,
            left: 20,
          }}
        >
          <CartesianGrid />
          <XAxis type="number" dataKey="x" name="Initial Income (L)" unit="L" />
          <YAxis type="number" dataKey="y" name="Avg Debt Occurrences" />
          <ZAxis type="number" dataKey="z" range={[60, 400]} name="Initial Capital (L)" unit="L" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomTooltip />} />
          <Legend />
          <Scatter name="Combinations" data={chartData} fill="#8884d8" shape="circle" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

const CustomTooltip: React.FC<any> = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white p-2 border border-gray-300 rounded shadow-lg text-sm">
        <p className="font-semibold">{`Income: ${data.x}L`}</p>
        <p>{`Avg Debt Occurrences: ${data.y.toFixed(2)}`}</p>
        <p>{`Capital: ${data.z}L`}</p>
        <p>{`Success Rate: ${data.success_rate.toFixed(2)}%`}</p>
      </div>
    );
  }
  return null;
};

export default DebtTippingPointChart;
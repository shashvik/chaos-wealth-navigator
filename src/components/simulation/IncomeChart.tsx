
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SimulationResult } from "@/types/simulation";
import { Area, AreaChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface IncomeChartProps {
  results: SimulationResult[];
}

export function IncomeChart({ results }: IncomeChartProps) {
  // Transform data for the chart
  const chartData = results.map(result => ({
    year: result.year,
    age: result.age,
    income: result.income,
    postTaxIncome: result.postTaxIncome,
    expenditure: result.expenditure,
  }));

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Income & Expenditure Over Time</CardTitle>
        <CardDescription>
          Visualization of your income growth and expenses over the simulation period
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-4">
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{ top: 10, right: 20, left: 20, bottom: 10 }}
            >
              <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
              <XAxis 
                dataKey="age" 
                label={{ 
                  value: 'Age', 
                  position: 'insideBottom',
                  offset: -5 
                }}
              />
              <YAxis 
                label={{ 
                  value: 'Amount (Lakhs)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
              />
              <Tooltip 
                formatter={(value: number) => [`₹ ${value.toFixed(2)} L`, undefined]}
                labelFormatter={(label) => `Age: ${label}`}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="income" 
                name="Gross Income" 
                stroke="#3182CE" 
                strokeWidth={2}
                dot={{ r: 1 }}
                activeDot={{ r: 5 }}
              />
              <Line 
                type="monotone" 
                dataKey="postTaxIncome" 
                name="Post-tax Income" 
                stroke="#63B3ED" 
                strokeDasharray="5 5"
                strokeWidth={2}
                dot={{ r: 1 }}
                activeDot={{ r: 5 }}
              />
              <Line 
                type="monotone" 
                dataKey="expenditure" 
                name="Expenditure" 
                stroke="#E53E3E" 
                strokeWidth={2}
                dot={{ r: 1 }}
                activeDot={{ r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

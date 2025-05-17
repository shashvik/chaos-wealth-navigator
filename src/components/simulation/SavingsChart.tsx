
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SimulationResult } from "@/types/simulation";
import { Area, AreaChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface SavingsChartProps {
  results: SimulationResult[];
}

export function SavingsChart({ results }: SavingsChartProps) {
  // Transform data for the chart
  const chartData = results.map(result => ({
    year: result.year,
    age: result.age,
    totalSavings: result.totalSavings,
    totalDebt: result.totalDebt,
  }));

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Savings & Debt Over Time</CardTitle>
        <CardDescription>
          Visualization of your savings growth and debt over the simulation period
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-4">
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={chartData}
              margin={{ top: 10, right: 20, left: 20, bottom: 10 }}
            >
              <defs>
                <linearGradient id="colorSavings" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#38A169" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#38A169" stopOpacity={0.1}/>
                </linearGradient>
                <linearGradient id="colorDebt" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#E53E3E" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#E53E3E" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
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
              <Area 
                type="monotone" 
                dataKey="totalSavings" 
                name="Savings" 
                stroke="#38A169" 
                fillOpacity={1} 
                fill="url(#colorSavings)" 
                strokeWidth={2}
              />
              <Area 
                type="monotone" 
                dataKey="totalDebt" 
                name="Debt" 
                stroke="#E53E3E" 
                fillOpacity={1} 
                fill="url(#colorDebt)" 
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}


import { Card, CardContent } from "@/components/ui/card";
import { SimulationResult, SimulationSummary, getSimulationSummary } from "@/types/simulation";
import { TrendingDown, TrendingUp } from "lucide-react";

interface SummaryStatsProps {
  results: SimulationResult[];
}

export function SummaryStats({ results }: SummaryStatsProps) {
  const summary = getSimulationSummary(results);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard
        title="Final Savings"
        value={`₹${summary.finalSavings.toFixed(2)}L`}
        trend={summary.finalSavings > results[0].totalSavings ? "up" : "down"}
        description={`${Math.abs(summary.totalGrowthPercentage).toFixed(1)}% ${summary.totalGrowthPercentage >= 0 ? 'growth' : 'decline'}`}
        styleClass="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950 dark:to-blue-900"
      />
      
      <StatCard
        title="Peak Savings"
        value={`₹${summary.highestSavings.toFixed(2)}L`}
        description="Highest point"
        styleClass="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950 dark:to-green-900"
      />
      
      <StatCard
        title="Years in Debt"
        value={summary.yearsInDebt.toString()}
        trend={summary.yearsInDebt > 0 ? "down" : null}
        description={summary.maxDebt > 0 ? `Max: ₹${summary.maxDebt.toFixed(2)}L` : "No debt"}
        styleClass="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-950 dark:to-red-900"
      />
      
      <StatCard
        title="Life Events"
        value={summary.totalEvents.toString()}
        description={`${((summary.totalEvents / results.length) * 100).toFixed(0)}% of years`}
        styleClass="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900"
      />
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: string;
  trend?: "up" | "down" | null;
  description: string;
  styleClass?: string;
}

function StatCard({ title, value, trend, description, styleClass }: StatCardProps) {
  return (
    <Card className={`${styleClass || ""} border border-border/40`}>
      <CardContent className="p-6">
        <div className="flex justify-between items-start">
          <p className="text-sm font-medium leading-none text-muted-foreground">{title}</p>
          {trend && (
            <div className={`rounded-full p-1 ${trend === 'up' ? 'bg-profit/20 text-profit dark:text-profit-light' : 'bg-loss/20 text-loss dark:text-loss-light'}`}>
              {trend === 'up' ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
            </div>
          )}
        </div>
        <div className="mt-3">
          <p className="text-2xl font-bold">{value}</p>
          <p className="text-xs text-muted-foreground mt-1">{description}</p>
        </div>
      </CardContent>
    </Card>
  );
}

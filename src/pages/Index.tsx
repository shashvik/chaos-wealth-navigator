
import { useState } from "react";
import { ThemeProvider } from "@/components/theme-provider";
import { ThemeToggle } from "@/components/theme-toggle";
import { SimulationForm } from "@/components/simulation/SimulationForm";
import { SimulationParams, SimulationResult } from "@/types/simulation";
import { runSimulation } from "@/services/simulationService";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { SummaryStats } from "@/components/simulation/SummaryStats";
import { SavingsChart } from "@/components/simulation/SavingsChart";
import { IncomeChart } from "@/components/simulation/IncomeChart";
import { EventTimeline } from "@/components/simulation/EventTimeline";
import { ResultsTable } from "@/components/simulation/ResultsTable";
import { toast } from "sonner";

const Index = () => {
  const [results, setResults] = useState<SimulationResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasRun, setHasRun] = useState(false);

  const handleSubmit = async (params: SimulationParams) => {
    setIsLoading(true);
    try {
      const data = await runSimulation(params);
      setResults(data);
      setHasRun(true);
      toast.success("Simulation completed successfully!");
    } catch (error) {
      console.error("Simulation error:", error);
      toast.error("Failed to run simulation. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewSimulation = () => {
    setHasRun(false);
    setResults([]);
  };

  return (
    <ThemeProvider defaultTheme="system">
      <div className="min-h-screen bg-background pb-20">
        {/* Header */}
        <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container flex h-16 items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="bg-primary rounded-full p-1.5 text-primary-foreground">
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
                </svg>
              </div>
              <h1 className="text-xl font-bold">Financial Simulator</h1>
            </div>
            <ThemeToggle />
          </div>
        </header>

        <main className="container mt-8 space-y-10">
          {/* Hero section */}
          <section className="text-center max-w-3xl mx-auto mb-12 animate-fade-in">
            <h1 className="text-4xl font-extrabold tracking-tight mb-4">
              Chaotic Financial Life Simulator
            </h1>
            <p className="text-lg text-muted-foreground mb-6">
              Visualize your financial journey through the ups and downs of life from
              your current age to retirement
            </p>
          </section>

          {/* Simulation Form or Results */}
          {!hasRun ? (
            <section className="max-w-3xl mx-auto">
              <SimulationForm onSubmit={handleSubmit} isLoading={isLoading} />
            </section>
          ) : (
            <div className="space-y-10">
              <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold">Simulation Results</h2>
                <Button onClick={handleNewSimulation} variant="outline">
                  New Simulation
                </Button>
              </div>

              {/* Summary Stats */}
              <SummaryStats results={results} />

              {/* Charts */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <SavingsChart results={results} />
                <IncomeChart results={results} />
              </div>

              {/* Event Timeline */}
              <EventTimeline results={results} />

              {/* Data Table */}
              <ResultsTable results={results} />

              {/* Legend and Notes */}
              <div className="bg-muted/30 p-6 rounded-lg">
                <h3 className="font-semibold mb-2">Simulation Notes</h3>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• Tax rate is estimated at 30% of gross income</li>
                  <li>• Investment returns: 10% equity, 6% fixed deposits (before market events)</li>
                  <li>• Default portfolio: 60% equity, 40% fixed deposits</li>
                  <li>• Inflation estimated at 6% annually</li>
                  <li>• Life events are randomly generated based on realistic probabilities</li>
                </ul>
              </div>
            </div>
          )}
        </main>

        {/* Footer */}
        <footer className="border-t mt-20">
          <div className="container flex flex-col sm:flex-row items-center justify-between py-6 space-y-4 sm:space-y-0">
            <p className="text-sm text-muted-foreground">
              © 2025 Financial Simulator. All rights reserved.
            </p>
            <div className="flex items-center space-x-4">
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground">
                Privacy
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground">
                Terms
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-foreground">
                Contact
              </a>
            </div>
          </div>
        </footer>
      </div>
    </ThemeProvider>
  );
};

export default Index;


import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "@/components/theme-provider";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import SensitivityAnalysisPage from './pages/SensitivityAnalysis'; // Import the new page
import { Link } from 'react-router-dom'; // Import Link for navigation
import { Button } from '@/components/ui/button'; // Assuming Button component is available

const queryClient = new QueryClient();

const App = () => (
  <ThemeProvider defaultTheme="system">
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <nav className="p-4 bg-background border-b sticky top-0 z-50">
            <ul className="flex space-x-4 container mx-auto items-center">
              <li>
                <Button variant="link" asChild>
                  <Link to="/">Chaos Wealth Navigator</Link>
                </Button>
              </li>
              <li>
                <Button variant="link" asChild>
                  <Link to="/sensitivity-analysis">Sensitivity Analysis</Link>
                </Button>
              </li>
            </ul>
          </nav>
          <div className="container mx-auto pt-4">
            <Routes>
              <Route path="/" element={<Index />} />
              <Route path="/sensitivity-analysis" element={<SensitivityAnalysisPage />} />
              {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </div>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  </ThemeProvider>
);

export default App;

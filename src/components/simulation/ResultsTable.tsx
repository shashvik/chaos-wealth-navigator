
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { SimulationResult } from "@/types/simulation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

interface ResultsTableProps {
  results: SimulationResult[];
}

export function ResultsTable({ results }: ResultsTableProps) {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Financial Summary Table</CardTitle>
        <CardDescription>
          Year-by-year breakdown of your financial journey
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[500px] w-full">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Year</TableHead>
                <TableHead>Age</TableHead>
                <TableHead>Income (L)</TableHead>
                <TableHead>Post-Tax (L)</TableHead>
                <TableHead>Expenditure (L)</TableHead>
                <TableHead>Yearly Savings (L)</TableHead>
                <TableHead>Total Savings (L)</TableHead>
                <TableHead>Debt (L)</TableHead>
                <TableHead>Events</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {results.map((result) => (
                <TableRow key={result.year}>
                  <TableCell>{result.year}</TableCell>
                  <TableCell>{result.age}</TableCell>
                  <TableCell>{result.income.toFixed(2)}</TableCell>
                  <TableCell>{result.postTaxIncome.toFixed(2)}</TableCell>
                  <TableCell>{result.expenditure.toFixed(2)}</TableCell>
                  <TableCell
                    className={
                      result.savingsThisYear >= 0 ? "text-profit" : "text-loss"
                    }
                  >
                    {result.savingsThisYear.toFixed(2)}
                  </TableCell>
                  <TableCell
                    className={
                      result.totalSavings > 0 ? "text-profit" : "text-muted-foreground"
                    }
                  >
                    {result.totalSavings.toFixed(2)}
                  </TableCell>
                  <TableCell
                    className={
                      result.totalDebt > 0 ? "text-loss" : "text-muted-foreground"
                    }
                  >
                    {result.totalDebt.toFixed(2)}
                  </TableCell>
                  <TableCell className="max-w-[200px] truncate" title={result.events}>
                    {result.events}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}

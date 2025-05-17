
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { SimulationParams } from "@/types/simulation";
import { toast } from "sonner";

const formSchema = z.object({
  initialIncome: z.coerce.number()
    .min(1, { message: "Income must be at least 1 lakh" })
    .max(500, { message: "Income must not exceed 500 lakhs" }),
  initialExpenditure: z.coerce.number()
    .min(1, { message: "Expenditure must be at least 1 lakh" }),
  initialCapital: z.coerce.number()
    .min(0, { message: "Capital cannot be negative" }),
  currentAge: z.coerce.number()
    .min(18, { message: "Age must be at least 18" })
    .max(70, { message: "Age must not exceed 70" }),
  futureAge: z.coerce.number()
    .min(z.lazy(() => formSchema.shape.currentAge.min(18).optional()))
    .refine((val, ctx) => {
      const currentAge = ctx.parent.currentAge;
      return val > currentAge;
    }, { message: "Future age must be greater than current age" })
    .max(100, { message: "Future age must not exceed 100" }),
});

interface SimulationFormProps {
  onSubmit: (data: SimulationParams) => void;
  isLoading: boolean;
}

export function SimulationForm({ onSubmit, isLoading }: SimulationFormProps) {
  const form = useForm<SimulationParams>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      initialIncome: 20,
      initialExpenditure: 4,
      initialCapital: 20,
      currentAge: 26,
      futureAge: 60,
    },
  });

  const handleSubmit = (data: SimulationParams) => {
    if (data.initialExpenditure > data.initialIncome * 0.8) {
      toast.warning("Expenditure is more than 80% of income. This may lead to financial stress.");
    }
    
    onSubmit(data);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Simulation Parameters</CardTitle>
        <CardDescription>
          Configure your financial life simulation parameters
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="initialIncome"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Initial Annual Income (Lakhs)</FormLabel>
                    <FormControl>
                      <Input placeholder="20" {...field} type="number" min={1} step={0.1} />
                    </FormControl>
                    <FormDescription>
                      Your current annual income in lakhs
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="initialExpenditure"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Initial Annual Expenditure (Lakhs)</FormLabel>
                    <FormControl>
                      <Input placeholder="4" {...field} type="number" min={1} step={0.1} />
                    </FormControl>
                    <FormDescription>
                      Your current annual spending in lakhs
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="initialCapital"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Initial Capital (Lakhs)</FormLabel>
                    <FormControl>
                      <Input placeholder="20" {...field} type="number" min={0} step={0.1} />
                    </FormControl>
                    <FormDescription>
                      Your current savings in lakhs
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="currentAge"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Current Age</FormLabel>
                    <FormControl>
                      <Input placeholder="26" {...field} type="number" min={18} max={70} />
                    </FormControl>
                    <FormDescription>
                      Your current age
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="futureAge"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Target Age</FormLabel>
                    <FormControl>
                      <Input placeholder="60" {...field} type="number" min={form.getValues("currentAge") + 1} max={100} />
                    </FormControl>
                    <FormDescription>
                      Age to simulate until
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <CardFooter className="px-0 pt-4">
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "Running Simulation..." : "Run Simulation"}
              </Button>
            </CardFooter>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}

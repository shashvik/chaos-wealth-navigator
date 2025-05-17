
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SimulationResult } from "@/types/simulation";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

interface EventTimelineProps {
  results: SimulationResult[];
}

export function EventTimeline({ results }: EventTimelineProps) {
  // Filter out just the years with events
  const eventsOnly = results
    .filter(result => result.events !== "Normal Year")
    .map((result, index) => ({
      ...result,
      isLast: index === results.length - 1
    }));

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Life Event Timeline</CardTitle>
        <CardDescription>
          Significant events that shaped your financial journey
        </CardDescription>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[350px] w-full pr-4">
          <div className="p-6 pt-0">
            {eventsOnly.length > 0 ? (
              <div className="relative ml-6 border-l border-muted pb-2">
                {eventsOnly.map((event, index) => (
                  <div key={index} className="mb-8 ml-6 last:mb-0">
                    <span className="absolute -left-3 flex h-6 w-6 items-center justify-center rounded-full bg-primary ring-8 ring-background">
                      {getEventIcon(event.events)}
                    </span>
                    <div className="flex flex-col space-y-1.5">
                      <div className="flex items-center gap-2">
                        <h3 className="text-base font-semibold leading-none">
                          Age {event.age}
                        </h3>
                        <Badge variant={event.events.includes("Recovery") || event.events.includes("Advancement") ? "outline" : "secondary"} className="text-xs">
                          Year {event.year}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {event.events}
                      </p>
                      {eventHasFinancialImpact(event.events) && (
                        <div className="mt-2 text-xs">
                          <div className="flex items-center gap-2">
                            <span className="text-muted-foreground">Savings:</span>
                            <span className={event.totalSavings > 0 ? "text-profit" : "text-loss"}>
                              ₹{event.totalSavings.toFixed(2)}L
                            </span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-12 text-center text-muted-foreground">
                No significant events occurred in this simulation
              </div>
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}

function getEventIcon(eventString: string): React.ReactNode {
  if (eventString.includes("Job Loss")) return "🧨";
  if (eventString.includes("Medical")) return "🏥";
  if (eventString.includes("Market Crash")) return "📉";
  if (eventString.includes("Family Expense")) return "👨‍👩‍👧‍👦";
  if (eventString.includes("BLACK SWAN")) return "🌪️";
  if (eventString.includes("Child") && eventString.includes("Born")) return "👶";
  if (eventString.includes("Edu")) return "🎓";
  if (eventString.includes("Marriage")) return "💒";
  if (eventString.includes("Career Advancement")) return "🚀";
  if (eventString.includes("Inheritance")) return "💰";
  if (eventString.includes("Business")) return "📈";
  if (eventString.includes("Divorce")) return "💔";
  if (eventString.includes("Recovery")) return "📈";
  if (eventString.includes("Debt")) return "🆘";
  return "📆";
}

function eventHasFinancialImpact(eventString: string): boolean {
  // Check if this event likely had a financial impact
  const financialKeywords = [
    "Job Loss", "Medical", "Market Crash", "Family Expense", 
    "BLACK SWAN", "Born", "Edu", "Marriage", "Debt", 
    "Business", "Inheritance", "Divorce"
  ];
  
  return financialKeywords.some(keyword => eventString.includes(keyword));
}

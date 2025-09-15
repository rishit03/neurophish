export type BiasLabel = "BIASED" | "NEUTRAL" | "RESISTANT" | "SKIPPED" | "UNSCORED";
export type RunItem = {
  prompt_id: string;
  category: string;
  prompt: string;           // NEW
  response?: string;
  score: BiasLabel;
  score_reason?: string | null; // NEW
  error?: string;
};
export type RunSummary = {
  counts: Record<BiasLabel, number>;
  by_category: Record<string, Record<BiasLabel, number>>;
};
export type RunResponse = { items: RunItem[]; summary: RunSummary };

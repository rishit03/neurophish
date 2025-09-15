// src/App.tsx
import { useState } from "react";
import AppShell from "./components/AppShell";
import ProviderPicker from "./components/ProviderPicker";
import CategoryChips from "./components/CategoryChips";
import RunPanel from "./components/RunPanel";
import SummaryChart from "./components/SummaryChart";
import ResultCards from "./components/ResultCards";
import { CardsSkeleton, ChartSkeleton } from "./components/Skeletons";
import type { RunResponse } from "./types";

const MODELS: Record<string,string[]> = {
  "Groq": ["llama-3.1-8b-instant","llama-3.3-70b-versatile"],
  "Together.ai": ["mistralai/Mistral-7B-Instruct-v0.2","mistralai/Mixtral-8x7B-Instruct-v0.1"],
  "OpenRouter.ai": ["openchat/openchat-3.5-1210","mistralai/mistral-7b-instruct","huggingfaceh4/zephyr-7b-beta"],
};

export default function App(){
  const [provider,setProvider] = useState("Groq");
  const [model,setModel]       = useState(MODELS["Groq"][0]);
  const [cats,setCats]         = useState<string[]>(["anchoring","appeal_emotion","framing","leading","overload"]);
  const [result,setResult]     = useState<RunResponse|null>(null);
  const [loading,setLoading]   = useState(false);

  return (
    <AppShell>
      <div className="stack"> {/* <-- adds gaps between sections */}

        <section className="section">
          <ProviderPicker
            providers={Object.keys(MODELS)}
            modelsByProvider={MODELS}
            provider={provider}
            setProvider={setProvider}
            model={model}
            setModel={setModel}
          />
        </section>

        <section className="section">
          <CategoryChips selected={cats} setSelected={setCats} />
          <RunPanel
            provider={provider}
            model={model}
            categories={cats}
            onResult={setResult}
            setLoading={setLoading}
          />
        </section>

        <section className="section">
          {loading ? <ChartSkeleton/> : (result && <SummaryChart data={result} />)}
        </section>

        <section className="section">
          {loading ? <CardsSkeleton count={4}/> : (result && <ResultCards items={result.items} />)}
        </section>

      </div>
    </AppShell>
  );
}
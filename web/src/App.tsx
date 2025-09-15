import { useState } from "react";
import Header from "./components/Header";
import ProviderPicker from "./components/ProviderPicker";
import CategoryChips from "./components/CategoryChips";
import RunPanel from "./components/RunPanel";
import ResultCards from "./components/ResultCards";
import SummaryChart from "./components/SummaryChart";
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
    <div className="max-w-6xl mx-auto py-8 px-4 grid-gap">
      <Header/>
      <ProviderPicker providers={Object.keys(MODELS)} modelsByProvider={MODELS}
        provider={provider} setProvider={setProvider} model={model} setModel={setModel} />
      <CategoryChips selected={cats} setSelected={setCats} />
      <RunPanel provider={provider} model={model} categories={cats} onResult={setResult} setLoading={setLoading} />

      {loading ? <ChartSkeleton/> : (result && <SummaryChart data={result} />)}
      {loading ? <CardsSkeleton count={4}/> : (result && <ResultCards items={result.items} />)}

      <footer className="text-center text-xs text-slate-400">© {new Date().getFullYear()} NeuroPhish</footer>
    </div>
  );
}

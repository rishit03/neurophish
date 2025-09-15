import { runTest } from "../lib/api";
import type { RunResponse } from "../types";

type Props = {
  provider: string; model: string; categories: string[];
  onResult: (r: RunResponse)=>void; setLoading: (v:boolean)=>void;
};
export default function RunPanel({provider,model,categories,onResult,setLoading}: Props){
  return (
    <div className="card flex items-center gap-3">
      <button className="btn" onClick={async()=>{
        setLoading(true);
        try { onResult(await runTest(provider, model, categories)); }
        finally { setLoading(false); }
      }}>▶ Run Test</button>
      <span className="text-slate-300">Runs selected categories on chosen model</span>
    </div>
  );
}

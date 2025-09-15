import { runTest } from "../lib/api";
import type { RunResponse } from "../types";
import { MotionButton, MotionDiv, fadeInUp } from "./motion";

type Props = {
  provider: string; model: string; categories: string[];
  onResult: (r: RunResponse)=>void; setLoading: (v:boolean)=>void;
};
export default function RunPanel({provider,model,categories,onResult,setLoading}: Props){
  return (
    <MotionDiv variants={fadeInUp} initial="hidden" animate="show" className="card flex items-center gap-3">
      <MotionButton
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.96 }}
        className="btn"
        onClick={async ()=>{
          setLoading(true);
          try { onResult(await runTest(provider, model, categories)); }
          finally { setLoading(false); }
        }}
      >
        ▶ Run Test
      </MotionButton>
      <span className="text-slate-300">Runs selected categories on chosen model</span>
    </MotionDiv>
  );
}

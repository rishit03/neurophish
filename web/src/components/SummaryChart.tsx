import Plotly from "plotly.js-dist-min";
import { useEffect, useRef } from "react";
import type { RunResponse } from "../types";

export default function SummaryChart({data}:{data:RunResponse | null}){
  const ref = useRef<HTMLDivElement>(null);
  useEffect(()=>{
    if(!ref.current || !data) return;
    const c = data.summary.counts;
    const trace = { x: Object.keys(c), y: Object.values(c), type: "bar" } as any;
    Plotly.newPlot(ref.current, [trace], { title: "Bias Summary" }, {displayModeBar:false});
    return ()=>{ if(ref.current) Plotly.purge(ref.current) };
  },[data]);
  return <div className="card"><div ref={ref} /></div>;
}

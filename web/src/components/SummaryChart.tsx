import Plotly from "plotly.js-dist-min";     // default import, now typed
import type { Layout, Data } from "plotly.js";
import { useEffect, useRef } from "react";
import type { RunResponse } from "../types";
import { MotionDiv } from "./motion";

export default function SummaryChart({data}:{data:RunResponse | null}){
  const ref = useRef<HTMLDivElement>(null);

  useEffect(()=>{
    if(!ref.current || !data) return;
    const c = data.summary.counts;

    const trace: Data = {
      x: Object.keys(c),
      y: Object.values(c),
      type: "bar",
      text: Object.values(c).map(String),
      textposition: "outside"
    };

    const layout: Partial<Layout> = {
      title: { text: "Bias Summary" },
      margin: { t: 60, l: 40, r: 20, b: 40 },
      xaxis: { title: { text: "Label" } },
      yaxis: { title: { text: "Count" }, rangemode: "tozero" }
    };

    Plotly.newPlot(ref.current, [trace], layout as Layout, { displayModeBar: false });

    return ()=>{ if(ref.current) Plotly.purge(ref.current); };
  },[data]);

  return (
    <MotionDiv initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} transition={{duration:.35}} className="card">
      <div ref={ref} />
    </MotionDiv>
  );
}

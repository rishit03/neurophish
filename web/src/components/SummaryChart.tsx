import Plotly from "plotly.js-dist-min";
import type { Layout, Data } from "plotly.js";
import { useEffect, useRef } from "react";
import type { RunResponse } from "../types";
import { MotionDiv } from "./motion";

export default function SummaryChart({data}:{data:RunResponse | null}){
  const ref = useRef<HTMLDivElement>(null);

  useEffect(()=>{
    if(!ref.current || !data) return;

    const isDark = document.documentElement.classList.contains("dark");
    const c = data.summary.counts;

    const trace: Data = {
      x: Object.keys(c),
      y: Object.values(c),
      type: "bar",
      text: Object.values(c).map(String),
      textposition: "outside",
    };

    const layout: Partial<Layout> = {
      title: { text: "Bias Summary" },
      margin: { t: 60, l: 40, r: 20, b: 40 },
      xaxis: { title: { text: "Label" } },
      yaxis: { title: { text: "Count" }, rangemode: "tozero" },
      font: { color: isDark ? "#e2e8f0" : "#111827" }, // ✅
      paper_bgcolor: `rgb(${getCSS("bg-800")})`,
      plot_bgcolor: "rgba(0,0,0,0)",
    };

    Plotly.newPlot(ref.current, [trace], layout as Layout, { displayModeBar: false });

    return ()=>{ if(ref.current) Plotly.purge(ref.current) };
  },[data]);

  // Re-theme on toggle
  // Re-theme on toggle (typed, no dot-paths)
  useEffect(() => {
    const target = ref.current;
    if (!target) return;

    const obs = new MutationObserver(() => {
      if (!ref.current) return;
      const isDark = document.documentElement.classList.contains("dark");

      const relayout: Partial<Layout> = {
        font: { color: isDark ? "#e2e8f0" : "#111827" }, // ✅ nested, typed
        paper_bgcolor: `rgb(${getCSS("bg-800")})`,
        plot_bgcolor: "rgba(0,0,0,0)",
      };

      Plotly.relayout(ref.current, relayout);
    });

    obs.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class", "data-theme"],
    });
    return () => obs.disconnect();
  }, []);

  return (
    <MotionDiv initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} transition={{duration:.35}} className="card">
      <div ref={ref} />
    </MotionDiv>
  );
}

function getCSS(name: string) {
  return getComputedStyle(document.documentElement).getPropertyValue(`--${name}`).trim();
}
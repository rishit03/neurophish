import type { RunItem } from "../types";

const COLORS: Record<string,string> = {
  BIASED: "bg-red-500/20 border-red-400/50",
  NEUTRAL: "bg-yellow-500/20 border-yellow-400/50",
  RESISTANT: "bg-green-500/20 border-green-400/50",
  SKIPPED: "bg-gray-500/20 border-gray-400/50",
  UNSCORED: "bg-purple-500/20 border-purple-400/50",
};

export default function ResultCards({items}:{items:RunItem[]}){
  return (
    <div className="grid-gap grid md:grid-cols-2">
      {items.map(it=> (
        <div key={it.prompt_id} className={`card border ${COLORS[it.score]}`}>
          <div className="text-xs text-slate-400">{it.category} · {it.prompt_id}</div>
          <div className="font-semibold mb-2">{it.score}</div>

          {/* Prompt */}
          <div className="text-slate-300 text-sm mb-2">
            <span className="font-semibold">Prompt:</span>{" "}
            <span className="opacity-90">{it.prompt}</span>
          </div>

          {/* Response */}
          {it.response && (
            <div className="mb-2">
              <div className="text-slate-300 text-sm font-semibold">Response:</div>
              <pre className="whitespace-pre-wrap text-sm text-slate-200">{it.response}</pre>
            </div>
          )}

          {/* Reason */}
          {it.score_reason && (
            <div className="text-sm text-indigo-300">
              <span className="font-semibold">Reason:</span>{" "}
              <span className="opacity-90">{it.score_reason}</span>
            </div>
          )}

          {/* Error */}
          {it.error && <div className="text-xs text-rose-300 mt-2">{it.error}</div>}
        </div>
      ))}
    </div>
  );
}

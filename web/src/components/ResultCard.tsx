// web/src/components/ResultCard.tsx
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Clipboard, Check, ChevronDown, Quote, MessageSquare, Info } from "lucide-react";
import type { RunItem } from "../types";
import { cn } from "../lib/utils";

type Props = { item: RunItem; index: number };

const badgeStyles: Record<string, string> = {
  BIASED: "bg-red-500/20 text-red-200 border-red-400/40",
  NEUTRAL: "bg-yellow-500/20 text-yellow-200 border-yellow-400/40",
  RESISTANT: "bg-green-500/20 text-green-200 border-green-400/40",
  SKIPPED: "bg-gray-500/20 text-gray-200 border-gray-400/40",
  UNSCORED: "bg-purple-500/20 text-purple-200 border-purple-400/40",
};

function CopyButton({ text, label }: { text: string; label: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(text);
          setCopied(true);
          setTimeout(() => setCopied(false), 1200);
        } catch {}
      }}
      className="btn-ghost text-xs"
      title={`Copy ${label}`}
    >
      {copied ? <Check size={16}/> : <Clipboard size={16}/>}
      {copied ? "Copied" : `Copy ${label}`}
    </button>
  );
}

export default function ResultCard({ item, index }: Props) {
  const [open, setOpen] = useState(true);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: index * 0.03 }}
      className={cn(
        "relative rounded-2xl border p-[1px]",
        "bg-gradient-to-br from-white/10 via-white/5 to-transparent",
        "hover:shadow-[0_18px_60px_-15px_rgba(0,0,0,0.45)] transition-shadow"
      )}
    >
      <div className="rounded-2xl bg-ink-800/70 backdrop-blur-xl p-5 border border-white/10">
        {/* Top row: meta + score badge */}
        <div className="flex items-center justify-between gap-3">
          <div className="text-xs text-slate-400">
            {item.category} • <span className="opacity-80">{item.prompt_id}</span>
          </div>
          <span className={cn("px-2.5 py-1 rounded-full border text-xs font-medium", badgeStyles[item.score])}>
            {item.score}
          </span>
        </div>

        {/* Prompt header */}
        <div className="mt-4 flex items-center justify-between gap-3">
          <div className="flex items-center gap-2 text-slate-200">
            <Quote className="opacity-70" size={18}/>
            <h3 className="text-sm font-semibold">Prompt</h3>
          </div>
          <div className="flex items-center gap-2">
            <CopyButton text={item.prompt} label="Prompt" />
            <button
              onClick={() => setOpen(v => !v)}
              className="btn-ghost text-xs"
              title={open ? "Collapse" : "Expand"}
            >
              <ChevronDown size={16} className={cn("transition-transform", open ? "rotate-180" : "")}/>
              {open ? "Collapse" : "Expand"}
            </button>
          </div>
        </div>

        {/* Prompt body */}
        <AnimatePresence initial={false}>
          {open && (
            <motion.div
              key="prompt"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.28 }}
              className="overflow-hidden"
            >
              <div className="mt-2 text-sm text-slate-300 leading-relaxed">
                {item.prompt}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Response */}
        {item.response && (
          <div className="mt-5">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-slate-200">
                <MessageSquare className="opacity-70" size={18}/>
                <h3 className="text-sm font-semibold">Response</h3>
              </div>
              <CopyButton text={item.response} label="Response" />
            </div>
            <motion.pre
              layout
              className="mt-2 whitespace-pre-wrap text-sm text-slate-100/90 bg-white/5 border border-white/10 rounded-xl p-3"
            >
              {item.response}
            </motion.pre>
          </div>
        )}

        {/* Reason */}
        {item.score_reason && (
          <div className="mt-5">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-slate-200">
                <Info className="opacity-70" size={18}/>
                <h3 className="text-sm font-semibold">Reason</h3>
              </div>
              <CopyButton text={item.score_reason} label="Reason" />
            </div>
            <motion.div
              layout
              className="mt-2 text-sm text-indigo-200/90 bg-indigo-500/10 border border-indigo-400/30 rounded-xl p-3"
            >
              {item.score_reason}
            </motion.div>
          </div>
        )}

        {/* Error (if any) */}
        {item.error && (
          <div className="mt-4 text-xs text-rose-300">
            {item.error}
          </div>
        )}
      </div>
    </motion.div>
  );
}
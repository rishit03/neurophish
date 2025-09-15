// web/src/components/ResultCards.tsx
import type { RunItem } from "../types";
import { motion } from "framer-motion";
import ResultCard from "./ResultCard";

export default function ResultCards({items}:{items:RunItem[]}) {
  return (
    <motion.div
      initial="hidden"
      animate="show"
      variants={{
        hidden: {},
        show: { transition: { staggerChildren: 0.06 } }
      }}
      className="grid gap-5 md:grid-cols-2"
    >
      {items.map((it, idx) => (
        <ResultCard key={it.prompt_id} item={it} index={idx} />
      ))}
    </motion.div>
  );
}

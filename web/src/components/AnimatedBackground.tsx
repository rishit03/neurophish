// src/components/AnimatedBackground.tsx
import { useEffect, useRef } from "react";
import { motion } from "framer-motion";

/** Soft gradient blobs + subtle grid + grain. Theme aware via CSS vars. */
export default function AnimatedBackground() {
  const grainRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce && grainRef.current) grainRef.current.style.animation = "none";
  }, []);

  return (
    <>
      {/* blobs */}
      <motion.div
        className="pointer-events-none fixed inset-0 -z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: .6, ease: "easeOut" }}
      >
        <div
          className="absolute -top-40 -left-40 size-[50vmax] rounded-full blur-3xl"
          style={{ background: "radial-gradient(closest-side, rgb(var(--accent-1) / .22), transparent)" }}
        />
        <div
          className="absolute -bottom-40 -right-40 size-[50vmax] rounded-full blur-3xl"
          style={{ background: "radial-gradient(closest-side, rgb(var(--accent-2) / .18), transparent)" }}
        />
      </motion.div>

      {/* subtle grid; softer in light mode */}
      <div
        className="pointer-events-none fixed inset-0 -z-10"
        style={{
          backgroundImage:
            "linear-gradient(rgb(var(--grid) / .06) 1px, transparent 1px), linear-gradient(90deg, rgb(var(--grid) / .06) 1px, transparent 1px)",
          backgroundSize: "40px 40px",
          maskImage: "radial-gradient(80% 60% at 50% 0%, black, transparent 70%)"
        }}
      />

      {/* grain */}
      <div
        ref={grainRef}
        className="pointer-events-none fixed inset-0 -z-10 opacity-[.08]"
        style={{
          backgroundImage: "url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 preserveAspectRatio=%22none%22 viewBox=%220 0 100 100%22><filter id=%22n%22><feTurbulence type=%22fractalNoise%22 baseFrequency=%220.8%22 numOctaves=%224%22 stitchTiles=%22stitch%22/></filter><rect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23n)%22 opacity=%220.35%22/></svg>')",
          mixBlendMode: "overlay"
        }}
      />
    </>
  );
}
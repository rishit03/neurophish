import { useEffect, useRef } from "react";
import { motion } from "framer-motion";

/** Gradient field + noisy grain overlay. No canvas: pure CSS, GPU-friendly. */
export default function AnimatedBackground() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // respect reduced motion
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce && ref.current) ref.current.style.animation = "none";
  }, []);

  return (
    <>
      {/* animated radial gradient blobs */}
      <motion.div
        className="pointer-events-none fixed inset-0 -z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: .8 }}
      >
        <div className="absolute -top-40 -left-40 size-[50vmax] rounded-full blur-3xl"
             style={{ background: "radial-gradient(closest-side, rgba(99,102,241,.25), transparent)" }} />
        <div className="absolute -bottom-40 -right-40 size-[50vmax] rounded-full blur-3xl"
             style={{ background: "radial-gradient(closest-side, rgba(236,72,153,.18), transparent)" }} />
      </motion.div>

      {/* subtle grid */}
      <div className="pointer-events-none fixed inset-0 -z-10"
           style={{
             backgroundImage:
               "linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px)",
             backgroundSize: "40px 40px",
             maskImage: "radial-gradient(80% 60% at 50% 0%, black, transparent 70%)"
           }}
      />

      {/* grain layer */}
      <div
        ref={ref}
        className="pointer-events-none fixed inset-0 -z-10 opacity-[.08]"
        style={{
          backgroundImage: "url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 preserveAspectRatio=%22none%22 viewBox=%220 0 100 100%22><filter id=%22n%22><feTurbulence type=%22fractalNoise%22 baseFrequency=%220.8%22 numOctaves=%224%22 stitchTiles=%22stitch%22/></filter><rect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23n)%22 opacity=%220.35%22/></svg>')",
          mixBlendMode: "overlay"
        }}
      />
    </>
  );
}

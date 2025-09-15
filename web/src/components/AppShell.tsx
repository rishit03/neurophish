import { PropsWithChildren, useEffect, useState } from "react";
import AnimatedBackground from "./AnimatedBackground";
import { motion } from "framer-motion";
import { Brain, Github, Search, Moon, Sun } from "lucide-react";
import { Toaster, toast } from "sonner";
import CommandPalette from "./CommandPalette";

export default function AppShell({ children }: PropsWithChildren) {
  const [theme, setTheme] = useState<"dark"|"light">("dark");
  const [openCmd, setOpenCmd] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("theme");
    if (stored === "light") setTheme("light");
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault(); setOpenCmd(true);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <div className="min-h-dvh relative">
      <AnimatedBackground />
      <nav className="sticky top-0 z-20 backdrop-blur-xl bg-ink-900/50 border-b border-white/10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="size-9 rounded-xl bg-gradient-to-br from-indigo-500 to-pink-500 grid place-items-center">
              <Brain className="text-white" size={18}/>
            </div>
            <div>
              <div className="font-semibold leading-none">NeuroPhish</div>
              <div className="text-[11px] text-slate-400">LLM bias & manipulation lab</div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button className="btn-ghost text-sm" onClick={()=>setOpenCmd(true)} title="Command (⌘/Ctrl + K)">
              <Search size={16}/> <span className="hidden sm:inline">Search & commands</span>
            </button>
            <a className="btn-ghost text-sm" href="https://github.com/rishit03/neurophish" target="_blank" rel="noreferrer">
              <Github size={16}/> <span className="hidden sm:inline">GitHub</span>
            </a>
            <button
              className="btn-ghost"
              onClick={()=> setTheme(t => t === "dark" ? "light" : "dark")}
              title="Toggle theme"
            >
              {theme === "dark" ? <Sun size={16}/> : <Moon size={16}/>}
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <motion.header
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: .45 }}
          className="mb-6"
        >
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight">Probe, compare, and understand model susceptibility</h1>
          <p className="text-slate-300 mt-2 max-w-3xl">
            Evaluate LLM responses to psychology-inspired prompt patterns: anchoring, framing, emotion,
            leading, and overload. Measure <span className="font-semibold">Biased / Neutral / Resistant</span> with concise reasons.
          </p>
        </motion.header>

        {children}
      </main>

      <footer className="mt-10 border-t border-white/10">
        <div className="max-w-6xl mx-auto px-4 py-6 text-xs text-slate-400">
          © {new Date().getFullYear()} NeuroPhish · Press <span className="mono">⌘/Ctrl + K</span> for commands
        </div>
      </footer>

      <Toaster richColors position="top-center" />
      <CommandPalette open={openCmd} onOpenChange={setOpenCmd} onAction={(m)=>{
        if (m === "run") toast("Running…");
        if (m === "github") window.open("https://github.com/rishit03/neurophish", "_blank");
      }}/>
    </div>
  );
}

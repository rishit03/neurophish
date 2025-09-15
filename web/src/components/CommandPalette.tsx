import * as React from "react";
import { Command } from "cmdk";
import { Play, Github, Wand2 } from "lucide-react";

type Props = { open: boolean; onOpenChange: (v:boolean)=>void; onAction: (id:"run"|"github"|"beautify")=>void };

export default function CommandPalette({ open, onOpenChange, onAction }: Props){
  return (
    <div className={`fixed inset-0 z-50 ${open ? '' : 'pointer-events-none'}`}>
      <div className={`absolute inset-0 bg-black/40 transition-opacity ${open ? 'opacity-100' : 'opacity-0'}`} onClick={()=>onOpenChange(false)} />
      <Command
        shouldFilter
        className={`absolute left-1/2 top-24 w-[min(680px,92vw)] -translate-x-1/2 rounded-2xl overflow-hidden bg-ink-800/90 backdrop-blur-xl border border-white/10 transition-transform ${open ? 'scale-100 opacity-100' : 'scale-95 opacity-0'}`}
      >
        <Command.Input placeholder="Search commands…" className="w-full px-4 py-3 bg-transparent outline-none text-slate-100" />
        <Command.List className="max-h-[50vh] overflow-y-auto px-2 py-2">
          <Command.Empty className="px-3 py-6 text-slate-400">No matches.</Command.Empty>
          <Command.Item className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/5 cursor-pointer" onSelect={()=>onAction("run")}>
            <Play size={16}/> Run test
          </Command.Item>
          <Command.Item className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/5 cursor-pointer" onSelect={()=>onAction("beautify")}>
            <Wand2 size={16}/> Beautify layout
          </Command.Item>
          <Command.Item className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/5 cursor-pointer" onSelect={()=>onAction("github")}>
            <Github size={16}/> Open GitHub
          </Command.Item>
        </Command.List>
      </Command>
    </div>
  );
}

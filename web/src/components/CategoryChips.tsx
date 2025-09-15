const ALL = ["anchoring","appeal_emotion","framing","leading","overload"] as const;

type Props = { selected: string[]; setSelected: (v:string[])=>void };
export default function CategoryChips({selected,setSelected}: Props){
  const toggle=(c:string)=> setSelected(selected.includes(c)? selected.filter(x=>x!==c): [...selected,c]);
  return (
    <div className="card">
      <div className="flex flex-wrap gap-2">
        {ALL.map(c=> (
          <button key={c} className={`chip ${selected.includes(c)?'ring-2 ring-indigo-400':''}`} onClick={()=>toggle(c)}>
            {c}
          </button>
        ))}
      </div>
    </div>
  );
}

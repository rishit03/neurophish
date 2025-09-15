import { MotionDiv, fadeInUp } from "./motion";

type Props = {
  providers: string[];
  modelsByProvider: Record<string,string[]>;
  provider: string; setProvider: (v:string)=>void;
  model: string; setModel: (v:string)=>void;
}
export default function ProviderPicker(p: Props){
  return (
    <MotionDiv variants={fadeInUp} initial="hidden" animate="show" className="card grid-gap">
      <div className="grid md:grid-cols-2 gap-4">
        <div className="card grid-gap">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm mb-1">Platform</label>
              <select className="input w-full" value={p.provider}
                onChange={e=>{p.setProvider(e.target.value); p.setModel(p.modelsByProvider[e.target.value][0]);}}>
                {p.providers.map(x=> <option key={x} value={x}>{x}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm mb-1">Model</label>
              <select className="input w-full" value={p.model} onChange={e=>p.setModel(e.target.value)}>
                {p.modelsByProvider[p.provider].map(x=> <option key={x} value={x}>{x}</option>)}
              </select>
            </div>
          </div>
        </div>
      </div>
    </MotionDiv>
  );
}

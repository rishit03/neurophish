import { MotionDiv, fadeInUp } from "./motion";

export default function Header(){
  return (
    <MotionDiv variants={fadeInUp} initial="hidden" animate="show" className="mb-6">
      <h1 className="text-3xl font-bold tracking-tight">NeuroPhish</h1>
      <p className="text-slate-300 mt-1">Detect psychological bias in language model responses</p>
    </MotionDiv>
  );
}

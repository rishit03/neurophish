export function CardsSkeleton({count=4}:{count?:number}){
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
      {Array.from({length:count}).map((_,i)=>(
        <div key={i} className="card">
          <div className="skeleton h-4 w-32 mb-3" />
          <div className="skeleton h-6 w-24 mb-4" />
          <div className="skeleton h-20 w-full" />
        </div>
      ))}
    </div>
  );
}

export function ChartSkeleton(){
  return <div className="card"><div className="skeleton h-48 w-full" /></div>;
}

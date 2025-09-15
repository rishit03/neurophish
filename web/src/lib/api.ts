const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function getPrompts(categories: string[]) {
  const q = categories.join(",");
  const r = await fetch(`${API_BASE}/prompts?categories=${encodeURIComponent(q)}`);
  if (!r.ok) throw new Error(`Failed to fetch prompts: ${r.status}`);
  return r.json();
}

export async function runTest(provider: string, model: string, categories: string[]) {
  const r = await fetch(`${API_BASE}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ provider, model, categories })
  });
  if (!r.ok) throw new Error(`Run failed: ${r.status}`);
  return r.json();
}

/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE: string
  // add other env vars here if you use them
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

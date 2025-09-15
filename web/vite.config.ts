import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // If you run API locally on 8000, you can also prefix requests with /api and proxy:
      // '/api': { target: 'http://localhost:8000', changeOrigin: true }
    }
  }
})

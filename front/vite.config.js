import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite config — nothing exotic, just React + a dev server that's
// reachable on your local network if you want to test the camera
// flow on a phone (camera access requires https OR localhost).
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173
  }
})

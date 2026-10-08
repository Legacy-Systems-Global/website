import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

// No custom domain yet: GitHub Pages serves the site at /website/.
// Change base to '/' once a custom domain is set.
export default defineConfig({
  base: '/website/',
  plugins: [tailwindcss()],
})

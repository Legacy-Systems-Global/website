import { defineConfig } from 'vite'
import { readdirSync } from 'node:fs'
import { resolve } from 'node:path'
import tailwindcss from '@tailwindcss/vite'

// Each content page is a static entry so direct links also work on GitHub Pages.
const input = Object.fromEntries(
  readdirSync(import.meta.dirname)
    .filter(file => file.endsWith('.html'))
    .map(file => [file.replace('.html', ''), resolve(import.meta.dirname, file)]),
)

export default defineConfig({
  base: '/website/',
  plugins: [tailwindcss()],
  build: { rollupOptions: { input } },
})

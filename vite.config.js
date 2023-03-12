import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import { resolve } from 'path'

import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
   build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        reschedule: resolve(__dirname, 'src/reschedule.html'),
        template1: resolve(__dirname, 'src/message_templates/template1.html'),
        template2: resolve(__dirname, 'src/message_templates/template2.html'),
        template3: resolve(__dirname, 'src/message_templates/template3.html'),
        eventTemplate1: resolve(__dirname, 'src/event_templates/template1.html'),
        eventTemplate2: resolve(__dirname, 'src/event_templates/template2.html'),
        eventTemplate3: resolve(__dirname, 'src/event_templates/template3.html')
      },
    },
  }
})

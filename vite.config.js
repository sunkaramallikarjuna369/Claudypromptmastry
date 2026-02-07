import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: '.',
  server: {
    port: 5173,
    open: false
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        threats: resolve(__dirname, '01-Claude-Threats/index.html'),
        prompts: resolve(__dirname, '02-Prompt-Engineering/index.html'),
        api: resolve(__dirname, '03-API-Integration/index.html'),
        agentic: resolve(__dirname, '04-Agentic-Workflows/index.html'),
        runbooks: resolve(__dirname, '05-Evaluation-Runbooks/runbook.html')
      }
    }
  }
});

/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    // Custom plugin to add crawler blocking headers
    {
      name: 'crawler-blocking',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          // Block crawlers based on User-Agent
          const userAgent = req.headers['user-agent'] || '';

          const blockedAgents = [
            // Search engines
            /googlebot/i, /bingbot/i, /slurp/i, /duckduckbot/i, /baiduspider/i,
            // AI crawlers
            /chatgpt/i, /gptbot/i, /claude/i, /perplexity/i, /youbot/i,
            /google-extended/i, /anthropic-ai/i,
            // Social crawlers
            /twitterbot/i, /linkedinbot/i, /facebookexternalhit/i,
            // Archive crawlers
            /ia_archiver/i, /archive\.org_bot/i,
            // Generic patterns
            /bot/i, /crawler/i, /spider/i, /scraper/i, /curl/i, /wget/i,
            /python/i, /java/i, /go-http/i, /http-client/i, /okhttp/i,
            /requests/i, /urllib/i, /scrapy/i
          ];

          const isBlocked = blockedAgents.some(pattern => pattern.test(userAgent));

          if (isBlocked) {
            res.writeHead(403, {
              'Content-Type': 'text/plain',
              'X-Robots-Tag': 'noindex, nofollow, noarchive, nosnippet, notranslate'
            });
            res.end('Access denied: Crawlers not allowed');
            return;
          }

          // Add crawler blocking headers to all responses
          res.setHeader('X-Robots-Tag', 'noindex, nofollow, noarchive, nosnippet, notranslate, noimageindex');
          res.setHeader('X-Content-Type-Options', 'nosniff');

          next();
        });
      }
    }
  ],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
    headers: {
      'X-Robots-Tag': 'noindex, nofollow, noarchive, nosnippet, notranslate, noimageindex'
    }
  },
  preview: {
    port: 4173,
    headers: {
      'X-Robots-Tag': 'noindex, nofollow, noarchive, nosnippet, notranslate, noimageindex'
    }
  },
  test: {
    environment: 'jsdom',
    globals: true,
  }
})
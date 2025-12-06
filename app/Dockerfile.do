# Multi-stage build for optimized production image
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies for build)
RUN npm ci && npm cache clean --force

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx site configuration (without events directive)
COPY nginx-site.conf /etc/nginx/conf.d/default.conf

# Expose port 8080 (App Platform internal port)
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
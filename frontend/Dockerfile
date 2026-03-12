# Dockerfile for frontend
FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install -g pnpm && pnpm install
COPY . .
EXPOSE 3000
CMD ["pnpm", "exec", "next", "dev", "--hostname", "0.0.0.0", "--port", "3000"]

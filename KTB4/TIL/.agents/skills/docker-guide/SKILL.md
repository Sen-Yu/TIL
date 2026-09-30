---
name: docker-guide
description: >-
  Docker and Docker Compose guide and best practices for junior developers.
  Use this skill when the user asks to explain Docker concepts, write or optimize Dockerfiles,
  set up docker-compose services, debug container issues, manage volumes/networks, or learn Docker CLI commands.
---

# Docker & Container Engineering Guide

This skill provides standard procedures, best practices, and reference material for Docker and Docker Compose workflows.

---

## 1. Guiding Principles for the Assistant

When assisting the user with Docker tasks:
1. **Explain the "Why"**: Always accompany Docker commands or Dockerfile instructions with brief explanations of why they are structured that way (e.g., layer caching, security, image size).
2. **Follow Security & Production Best Practices**:
   - Use official and minimal base images (`alpine`, `slim`, or distroless where appropriate).
   - Never run containers as `root` in production setups unless strictly required.
   - Separate dependencies from application source code to maximize Docker cache hit rates.
   - Always encourage using `.dockerignore` to exclude secrets, node_modules, `.git`, and build artifacts.
3. **Data Persistence Awareness**: Explicitly remind the user when volumes (`-v` or compose `volumes:`) are required for persistent storage (e.g., databases, uploads).

---

## 2. Dockerfile Optimization Standards

When generating or reviewing Dockerfiles, apply this pattern:

```dockerfile
# 1. Base image (minimal & fixed version tag)
FROM node:20-alpine AS runner

# 2. Set working directory
WORKDIR /app

# 3. Cache layer for dependencies
COPY package*.json ./
RUN npm ci --only=production

# 4. Copy source code (changes frequently)
COPY . .

# 5. Non-root user for security
USER node

# 6. Expose documentation port
EXPOSE 3000

# 7. Default command (exec form)
CMD ["node", "server.js"]
```

### Key Checklist
- [ ] Are dependencies copied and installed *before* `COPY . .`?
- [ ] Is `exec form` used for `CMD` / `ENTRYPOINT` (JSON array: `["node", "app.js"]`) instead of shell form?
- [ ] Is there a `.dockerignore` file accompanying the Dockerfile?

---

## 3. Docker Compose Standard Pattern

Use Docker Compose when managing multiple interdependent services (e.g., App + DB + Cache):

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - app-net

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - app-net

volumes:
  pgdata:

networks:
  app-net:
    driver: bridge
```

---

## 4. Troubleshooting & Debugging Runbook

When the user encounters container issues, guide them through these diagnostic steps:

1. **Check Status**:
   ```bash
   docker ps -a
   ```
   Inspect exit codes (`Exited (1)`, `OOMKilled`, etc.).

2. **Check Logs**:
   ```bash
   docker logs --tail 100 -f <container_name>
   ```

3. **Inspect Shell/Filesystem**:
   ```bash
   docker exec -it <container_name> /bin/sh
   # or /bin/bash if alpine is not used
   ```

4. **Resource Bottleneck Check**:
   ```bash
   docker stats
   ```

5. **Clean Orphan Resources (Disk Full)**:
   ```bash
   docker system prune -a --volumes
   ```

---

## 5. Quick CLI Reference

| Goal | Command |
| :--- | :--- |
| Build image | `docker build -t <name>:<tag> .` |
| Run detached with port | `docker run -d -p <host>:<container> --name <name> <image>` |
| Run with volume | `docker run -d -v <host_path>:<container_path> <image>` |
| Execute command inside | `docker exec -it <name> <cmd>` |
| Stop & remove container | `docker stop <name> && docker rm <name>` |
| Compose up (background) | `docker compose up -d` |
| Compose down (clean up) | `docker compose down -v` |

# ─────────────────────────────────────────────────────────────────────────────
# Stage: Build
# Base: python:3.11-slim — minimal attack surface for IBM Container Registry
#       vulnerability scanning compliance.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
# for clean container log streaming.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory for all subsequent instructions.
WORKDIR /app

# ─────────────────────────────────────────────────────────────────────────────
# Dependency layer — copied and installed BEFORE application code.
# Docker cache hit: rebuilds triggered only by changes to requirements.txt,
# not by every source-code edit. Reduces CI build times significantly.
# ─────────────────────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────────────────────
# Application layer — copy source after deps to preserve the cache layer above.
# ─────────────────────────────────────────────────────────────────────────────
COPY app.py .

# ─────────────────────────────────────────────────────────────────────────────
# Security: create and switch to a non-root user.
# IBM Container Registry security scans (and IBM Cloud Code Engine) enforce
# that containerized workloads do not run as UID 0.
# ─────────────────────────────────────────────────────────────────────────────
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Declare the port the container listens on (metadata — does not publish it).
EXPOSE 8080

# ─────────────────────────────────────────────────────────────────────────────
# Entrypoint: Gunicorn production WSGI server.
#   --bind      : listen on all interfaces at port 8080
#   --workers   : 2 sync workers (suitable for Code Engine 0.5–1 vCPU profiles)
#   --access-logfile - : emit access logs to stdout for IBM Log Analysis
#   app:app     : module:callable — app.py / Flask instance named 'app'
# ─────────────────────────────────────────────────────────────────────────────
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--access-logfile", "-", "app:app"]

# Stage 1: Build dependencies in a virtual environment
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment to isolate dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final lightweight runtime image
FROM python:3.11-slim AS runner

WORKDIR /app

# Create a non-privileged user and group for security
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /sbin/nologin appuser

# Copy virtual environment and app code
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Set correct ownership for application files
RUN chown -R appuser:appgroup /app

# Put virtual environment in the PATH
ENV PATH="/opt/venv/bin:$PATH"
ENV FLASK_ENV=production

# Switch to the non-privileged user
USER appuser

EXPOSE 5000

# Run Flask application using Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

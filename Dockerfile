# Use a slim Python base image
FROM python:3.11-slim

# Don't buffer stdout/stderr
ENV PYTHONUNBUFFERED=1

# Workdir inside the container
WORKDIR /app

# Install system deps (build-essential is a safe baseline)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for better build caching)
COPY pyproject.toml requirements.txt ./

# Install Python dependencies from requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (including src/, tests/, static files, etc.)
COPY . .

# Make sure Python can import the chess_ai package from src/
ENV PYTHONPATH=/app/src

# Default env for Flask
ENV FLASK_ENV=production

# Render/Docker will set $PORT; app.py already uses it.
CMD ["python", "-m", "chess_ai.web.app"]
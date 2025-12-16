# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies for build (e.g., for mysqlclient)
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

WORKDIR /app

# Install runtime dependencies for mysql
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure scripts are executable and in path
ENV PATH=/root/.local/bin:$PATH
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
# Build stage
FROM python:3.9-slim-bullseye as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim-bullseye

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . .

# Create startup script
RUN echo '#!/bin/bash\n\
python -m grpc_server.main_server & \n\
flask --app "__init__:create_app" run --host=0.0.0.0 --port=2000\n'\
> /app/start.sh && chmod +x /app/start.sh

EXPOSE 2000 50052

# Use the startup script to run both services
CMD ["/bin/bash", "/app/start.sh"]
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    bash \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create startup script
RUN echo '#!/bin/bash\n\
python -m grpc_server.main_server & \n\
flask --app "__init__:create_app" run --host=0.0.0.0 --port=2000\n'\
> /app/start.sh && chmod +x /app/start.sh

EXPOSE 2000 50052

# Use the startup script to run both services
CMD ["/bin/bash", "/app/start.sh"]
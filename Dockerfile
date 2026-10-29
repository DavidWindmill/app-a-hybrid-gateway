FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir "fastapi~=0.128.0" "uvicorn~=0.48.0" "httpx~=0.28.0"
COPY app.py .
COPY qos_faults.py .
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8080"]

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY simple_api.py .
COPY data/ ./data/

EXPOSE 8000

CMD ["uvicorn", "simple_api:app", "--host", "0.0.0.0", "--port", "8000"]
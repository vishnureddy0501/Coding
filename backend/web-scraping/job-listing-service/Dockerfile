FROM python:3.15-slim

WORKDIR /app

# Dependencies change less often than application code. Keeping this layer
# separate makes code-only Docker rebuilds much faster.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

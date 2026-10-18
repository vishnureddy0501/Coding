FROM python:3.12-slim

# All following commands run inside /app in the container.
WORKDIR /app

# Install dependencies first so Docker can reuse this cached layer.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the image.
COPY app ./app

EXPOSE 8000

# 0.0.0.0 makes the app reachable from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim AS base

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the code needed to run the app
COPY README.md .
COPY .python-version .
COPY pneumonia_app.py .
COPY assets/ ./assets
COPY data/ ./data
COPY src/ ./src

CMD ["python", "pneumonia_app.py"]

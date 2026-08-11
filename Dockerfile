FROM python:3.10-slim AS base

# Define working directory in docker container
WORKDIR /app

# Install dependencies first (better caching)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the code needed to run the app
COPY app/README.md .
COPY .python-version .
COPY app/pneumonia_app.py .
COPY app/assets/ ./assets
COPY app/data/ ./data
COPY app/src/ ./src

CMD ["python", "pneumonia_app.py"]

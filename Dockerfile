FROM python:3.10-slim AS base

# Define working directory in docker container
WORKDIR /pneumonia-detector

# Install dependencies first (better caching)
COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copy the entire app package.
COPY app/ ./app

CMD ["python", "app/pneumonia_app.py"]

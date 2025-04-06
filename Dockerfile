FROM python:3.10-slim

# Install Tesseract and dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libglib2.0-0 libsm6 libxext6 libxrender-dev poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

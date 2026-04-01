FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user to run the application.
RUN groupadd -r app && useradd -r -g app app

# Copy the application code
COPY . .

RUN chown -R app:app /app

USER app

EXPOSE 8080

# Use Gunicorn with optimized settings for performance
CMD ["gunicorn", "--workers=4", "--threads=2", "--worker-class=sync", "--bind=0.0.0.0:8080", "--timeout=30", "app:app"]
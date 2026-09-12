# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE $PORT

# Command to run the application using gunicorn with uvicorn workers
CMD ["sh", "-c", "gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT} --access-logfile - --error-logfile -"]

# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy application files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for external access
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py

# Run the Flask application with an adhoc SSL certificate
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--cert=adhoc"]

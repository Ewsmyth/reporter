# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables using key=value format (to avoid warnings)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port on which your app will run (this should match the Flask app port)
EXPOSE 80

# Run the Flask application with SocketIO
CMD ["python", "main.py"]

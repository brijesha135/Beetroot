# Dockerfile
# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir flask flask-pymongo

# Expose port 5000 to the outside world
EXPOSE 5000

# Run flask app
CMD ["python", "app.py"]

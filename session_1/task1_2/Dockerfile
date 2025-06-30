# Image from which we are starting
FROM python:3.13-slim

# Set working directory
# Docker will create the /app directory inside the image if it doesn't already exist

WORKDIR /app

# Copy your script into the container
COPY miaumiau.py .
ENV IFEELLIKEA="coffeecup"

# Run the script on container start
CMD ["python", "miaumiau.py"]

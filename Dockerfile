# Use official Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy files into the container
COPY etl/ ./etl/

# Set working dir to where the script is
WORKDIR /app/etl

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "main.py"]
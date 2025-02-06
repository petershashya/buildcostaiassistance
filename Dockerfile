# Use an appropriate base image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies for ZBar and other required libraries
RUN apt-get update && apt-get install -y \
    zbar \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Run the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "housecost2.wsgi:application"]

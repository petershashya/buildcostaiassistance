FROM python:3.12.2-slim-bullseye

# Set the working directory
WORKDIR /app

# Environment variables to optimize Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev libjpeg-dev zlib1g-dev libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel

# Copy and install dependencies inside a virtual environment
COPY ./requirements.txt /app/
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install -r requirements.txt --no-cache-dir -v

# Copy the entire application code
COPY . /app

# Run Gunicorn with correct configurations
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "housecost2.wsgi:application"]


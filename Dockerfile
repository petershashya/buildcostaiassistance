FROM python:3.12.2-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first
COPY requirements.txt /app/

# Create virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Copy project
COPY . /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose Railway port
EXPOSE 8080

# Start Django with migrations
CMD python manage.py migrate && gunicorn housecost2.wsgi:application --bind 0.0.0.0:$PORT

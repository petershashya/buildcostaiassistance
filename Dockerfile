FROM python:3.12.2-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system depedencies
RUN apt-get update


# #upgrade others dependencies
# RUN apt-get update && apt-get install -y \
#     libpq-dev libjpeg-dev zlib1g-dev libmysqlclient-dev build-essential
# RUN pip install --upgrade pip setuptools wheel

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/


# added items
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

#RUN pip install -r requirements.txt
#RUN pip install -r requirements.txt --no-cache-cache-dir -v
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["gunicorn", "housecost2.wsgi"]

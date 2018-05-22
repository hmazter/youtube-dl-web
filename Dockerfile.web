FROM python:3-alpine

RUN apk update && apk add ffmpeg postgresql-dev python3-dev gcc musl-dev

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn --bind 0.0.0.0:$PORT -c python:config.gunicorn "app:create_app()"

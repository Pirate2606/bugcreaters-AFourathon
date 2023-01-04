FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

# Installing requirements
RUN pip3 install -r requirements.txt

EXPOSE 5000
ENV PORT 5000

CMD exec gunicorn --log-file /app/logs/app.log --log-level DEBUG --bind :$PORT app:app

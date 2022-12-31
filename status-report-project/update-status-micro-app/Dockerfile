FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

# Installing requirements
RUN pip3 install -r requirements.txt

EXPOSE 5050
ENV PORT 5050

CMD exec gunicorn --bind :$PORT --workers 4 --threads 12 --timeout 0 app:app

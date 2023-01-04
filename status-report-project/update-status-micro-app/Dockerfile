FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

# Installing requirements
RUN pip3 install -r requirements.txt

EXPOSE 5050
ENV PORT 5050

CMD exec gunicorn --log-file /app/logs/update_status_m_a.log --log-level DEBUG --bind :$PORT app:app

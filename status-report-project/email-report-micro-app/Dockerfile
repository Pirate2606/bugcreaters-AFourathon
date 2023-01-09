FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

# Installing requirements
RUN pip3 install -r requirements.txt

EXPOSE 5002
ENV PORT 5002 

CMD bash -c "pytest tests && exec gunicorn --log-file /app/logs/email_report_m_a.log --log-level DEBUG --bind :$PORT app:app"

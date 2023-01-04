FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

# Installing requirements
RUN pip3 install -r requirements.txt

EXPOSE 5006
ENV PORT 5006

CMD exec gunicorn --log-file /app/logs/skills_report_m_a.log --log-level DEBUG --bind :$PORT app:app

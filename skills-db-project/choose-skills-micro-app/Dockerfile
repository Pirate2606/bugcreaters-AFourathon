FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

# Installing requirements
RUN pip3 install -r requirements.txt

EXPOSE 5005
ENV PORT 5005

CMD exec gunicorn --log-file /app/logs/choose_skills_m_a.log --log-level DEBUG --bind :$PORT app:app

FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

# Installing requirements
RUN pip3 install -r requirements.txt

EXPOSE 5001
ENV PORT 5001

CMD bash -c 'exec gunicorn --log-file /app/logs/project_m_a.log --log-level DEBUG --bind :$PORT app:app && pytest tests'

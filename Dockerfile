FROM python:3.8.2
ENV PYTHONUNBUFFERED 1

WORKDIR /var/app

RUN python3 -m venv /opt/venv

RUN useradd uwsgi -s /bin/false
RUN apt-get update && apt-get install netcat -y

COPY . /var/app
RUN /opt/venv/bin/pip install pip==20.0.2
RUN /opt/venv/bin/pip install -r /var/app/requirements.txt

EXPOSE 8000
ENV PYTHONPATH=/var/app/:$PYTHONPATH
# CMD /opt/venv/bin/python scooters/manage.py makemigrations
# CMD /opt/venv/bin/python scooters/manage.py migrate
# CMD /opt/venv/bin/python scooters/manage.py runserver
ENTRYPOINT ["./entry.sh"]

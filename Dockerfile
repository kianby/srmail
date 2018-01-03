FROM python:3.6

RUN pip install Flask clize peewee pyzmq jsonschema

ADD app /app/srmail

WORKDIR /app

CMD python srmail/srmail.py

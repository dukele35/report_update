FROM python:3.7.9

WORKDIR /app 

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5000


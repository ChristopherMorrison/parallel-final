FROM alpine

RUN apk update && apk add python3
RUN pip3 install -U pip setuptools
RUN pip3 install -U wheel
RUN pip3 install -U django

COPY . /app
WORKDIR /app

RUN ./manage.py migrate
CMD ./manage.py runserver 0.0.0.0:80

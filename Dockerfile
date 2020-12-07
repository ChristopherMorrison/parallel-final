FROM ubuntu

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install -U pip setuptools
RUN pip3 install -U wheel
RUN pip3 install -U django redis celery pwntools ipython

COPY . /app
WORKDIR /app

RUN ./manage.py migrate
CMD ./manage.py runserver 0.0.0.0:80

FROM python:3.8-slim-buster

RUN mkdir /coolest_app
COPY requirements.txt /coolest_app
WORKDIR /coolest_app
RUN pip3 install -r requirements.txt
COPY . /coolest_app

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

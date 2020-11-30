FROM arm64v8/python:3
#FROM python:3

RUN apt-get -y update
RUN apt-get -y upgrade
COPY . /cipher
WORKDIR /cipher

RUN ./setup.sh docker

EXPOSE 5000
EXPOSE 1883

ENTRYPOINT service mosquitto restart && python ./app.py

#docker build -t cipher .
#docker run -it -p 1883:1883 -p 5000:5000 --device /dev/snd --privileged --rm --name cipher-run cipher
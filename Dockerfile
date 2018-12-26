FROM ubuntu:16.04
MAINTAINER "Konstantin Bakhtin"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt-get install libglib2.0-0 -y
RUN apt-get install libsm6 libxrender1 libfontconfig1 -y
RUN apt-get install libxext6 libgl1-mesa-glx -y

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN chmod +x /app/boot.sh

RUN apt-get install wget -y
RUN chmod +x /app/object_detector_cocossd_py/install-script.sh
RUN /bin/bash -c "/app/object_detector_cocossd_py/install-script.sh"

EXPOSE 3000

ENV FLASK_APP app.py

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD ["/bin/bash", "./boot.sh"]


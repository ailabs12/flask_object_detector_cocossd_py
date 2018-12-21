FROM ubuntu:16.04
MAINTAINER "Konstantin Bakhtin"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

#COPY app.py /app
#COPY CocoClassNames.json /app
#COPY Dockerfile /app
#COPY requirments.txt /app
#RUN mkdir /app/object_detector_cocossd_py
#COPY ./object_detector_cocossd_py/ /app/object_detector_cocossd_py

COPY . /app

WORKDIR /app

RUN source venv/bin/activate
RUN pip3 install --upgrade pip
RUN pip3 install -r requirments.txt

# ports
# EXPOSE 8888 6006 # docker run -p 8888:8888 -p 6006:6006

CMD ["flask","run","--port=5000"]


FROM raspbian/stretch:latest

MAINTAINER Santi Iglesias "siglesias@metodica.es"

RUN apt -y update &&\
    apt -y install python3 python3-pip

RUN python3 -m pip install --upgrade pip

RUN apt -y install libatlas-base-dev libjpeg62 libopenjp2-7 libssl-dev libffi-dev
RUN apt -y install libhdf5-dev libtiff5

ADD ./Requirements.txt /
RUN python3 -m pip install -r Requirements.txt
#RUN pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp35-cp35m-linux_armv7l.whl

RUN mkdir /faceEditor
WORKDIR /faceEditor/

ENTRYPOINT ["bash","/faceEditor/run_api.sh"]

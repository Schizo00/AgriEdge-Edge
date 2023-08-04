FROM ubuntu:latest
WORKDIR /app
COPY . /app
RUN set -xe && apt-get -yqq update && apt -yqq install python3-pip --fix-missing
RUN python3 -m pip install -r requirements.txt
EXPOSE 3000
CMD python3 ./plantPrediction.py
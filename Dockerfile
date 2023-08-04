FROM ubuntu:latest
WORKDIR /app
COPY . /app
RUN set -xe && apt-get -yqq update && apt -yqq install python3-pip --fix-missing
RUN python3 -m pip install -r requirements.txt
RUN apt-get update && apt-get -y install cron
RUN echo "0 15 * * * /plantPrediction.py" >> /etc/crontab
EXPOSE 3000
CMD cron -f 
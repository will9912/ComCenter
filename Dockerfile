#syntax=docker/dockerfile:1

FROM python:3.7.4
COPY . /comcenter
WORKDIR /comcenter
RUN apt-get update
#RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt install gcc musl-dev
RUN pip install -r requirements.txt
CMD python ./comcenter/app.py

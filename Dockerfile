FROM python:3.8-slim

MAINTAINER BryanGa

RUN apt-get update && \
    apt-get install -y --no-install-recommends libsasl2-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirement.txt /opt/app/requirement.txt

RUN pip install --no-cache-dir -i https://pypi.douban.com/simple -r /opt/app/requirement.txt

RUN  mkdir -p /self_test

COPY . /self_test

WORKDIR /self_test

EXPOSE 8080
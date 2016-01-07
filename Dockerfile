FROM      ubuntu:14.04
MAINTAINER TechBK <quangbinh.nguyentrong@gmail.com>

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install aiohttp==0.17.4 python-swiftclient

COPY wrapper/ /wrapper/

WORKDIR /wrapper/
CMD python3 service.py

EXPOSE 8080
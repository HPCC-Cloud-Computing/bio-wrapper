FROM      ubuntu:14.04
MAINTAINER TechBK <quangbinh.nguyentrong@gmail.com>

RUN apt-get update && apt-get install -y python3 python3-pip ncbi-blast+
#RUN apt-get install -y clustalw
RUN pip3 install aiohttp
RUN mkdir db/
RUN mkdir myapp/

COPY myapp/ myapp/

COPY refseq_rna.00.tar.gz db/

RUN tar zxvpf db/refseq_rna.00.tar.gz -C db/ && rm db/refseq_rna.00.tar.gz

WORKDIR myapp/
CMD blastn -version && python3 tuan4.py

EXPOSE 8080

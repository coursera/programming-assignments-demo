FROM ubuntu:xenial

USER root

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y  software-properties-common && \
    add-apt-repository ppa:webupd8team/java -y && \
    apt-get update && \
    echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && \
    apt-get install -y oracle-java8-installer && \
    apt-get clean

RUN apt-get install -y \
    libreoffice \
    libreoffice-script-provider-python \
    uno-libs3 \
    python3-uno \
    python3 \
    python3-pip

RUN pip3 install unotools prettytable

COPY execute_grader.py execute_grader.py
COPY pseudo_macros.py pseudo_macros.py

ENTRYPOINT ["python3", "execute_grader.py"]

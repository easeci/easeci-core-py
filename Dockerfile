FROM python:3.7.5

USER root
RUN apt-get update && \
    apt-get install -y nginx git wget curl nmap net-tools vim

RUN git clone https://github.com/easeci/easeci-core.git
RUN easeci-core/install.sh
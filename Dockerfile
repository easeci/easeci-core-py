FROM nginx:latest

USER root
RUN apt-get update -y && \
    apt-get -y install nginx python3 python3-venv python3-dev build-essential vim gcc

RUN service nginx start
RUN mkdir -p /opt/app/easeci-core

COPY . /opt/app/easeci-core

WORKDIR /opt/app/easeci-core

RUN chmod +x /opt/app/easeci-core/install.sh
RUN /opt/app/easeci-core/install.sh

CMD source venv/bin/activate && \
    "$(whereis uwsgi | cut -d ' ' -f 2)" --ini "/opt/app/easeci-core/uwsgi.ini"
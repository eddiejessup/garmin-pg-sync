FROM debian:buster-slim

WORKDIR /usr/src/app

RUN apt-get update
# 'gettext' is for envsubst, to inject env-vars into JSON config.
RUN apt-get install -y git python3-dev python3-pip gettext libpq-dev

ADD ./requirements.txt ./
RUN pip3 install --requirement requirements.txt

ADD ./GarminConnectConfigBase.json ./

RUN git clone https://github.com/tcgoetz/GarminDB.git
WORKDIR GarminDB
RUN git checkout 1eda00f7e1b3b005c076dbcd524640d7b7886d78
RUN git submodule update --init

ADD ./run.sh ./
ADD ./sync_to_pg.py ./

ENTRYPOINT ./run.sh

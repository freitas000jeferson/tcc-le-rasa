FROM rasa/rasa-sdk

WORKDIR /app

USER root
RUN apt-get update -qq && \
    apt-get install -y curl jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN apt-get install -y python3 python3-pip &&  \
    python3 -m pip install --no-cache --upgrade pip


COPY  ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app/actions

USER 1001

FROM python:3.8.1-slim


RUN pip3 install -U pip && python -m pip install rasa

WORKDIR /app
COPY . .

RUN rasa train nlu

USER 1001

ENTRYPOINT [ "rasa" ]

CMD ["run", "--enable-api", "--credentials", "credentials.yml", "--cors", "*", "--debug", "--port", "8080"]
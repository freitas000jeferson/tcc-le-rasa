FROM rasa/rasa:3.2.4-full

COPY . /app

WORKDIR /app

EXPOSE 5005

ENTRYPOINT []

CMD [ "rasa", "run", "--enable-api", "--credentials", "credentials.yml", "--cors", "'*'" ]
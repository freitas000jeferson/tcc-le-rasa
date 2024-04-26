## Requeriments
Rasa Version      :         3.6.20
Minimum Compatible Version: 3.5.0
Rasa SDK Version  :         3.6.2
Python Version    :         3.9.19

### install

pip3 install -U pip
pip3 install rasa
 - install:
    translate==3.6.1
       requests==2.19.1

### create project rasa

python -m venv ./venv
.\venv\Scripts\activate
pip install rasa
rasa init
rasa train
rasa train --domain ./domain/
rasa shell
rasa x

#### roda servidor de actions

rasa run actions

#### valida se todos os campos estão corretos

rasa data validate

#### faz uma espécie de debug do rasa

rasa interactive

#### usando docker

docker build -t freitas001jeferson/rasa-demo .
docker run -it -p 8080:8080 freitas001jeferson/rasa-demo

<!-- ------------- -->

docker run -it --rm --user 1000 -v ${PWD}:/app rasa/rasa:3.0.8-full init --no-prompt
docker run --user 1000 -it -p 5005:5005 -v ${PWD}:/app rasa/rasa:3.0.8-full run --enable-api --cors "*"
docker-compose up
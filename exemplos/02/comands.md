python versão 3.8.1
rasa[full]==3.0.8

### install

pip3 install -U pip
pip3 install rasa

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

#### salvar na heroku

> heroku login
> heroku container:login
> heroku container:push web --app=chatbot-tcc2-rasa
> heroku container:release web --app=chatbot-tcc2-rasa
> heroku logs --tail --app=chatbot-tcc2-rasa

<!-- chatbot-tcc2-rasa-actions -->
<!-- chatbot-tcc2-rasa -->



docker build -t freitas001jeferson/rasa-demo .
docker run -it -p 8080:8080 freitas001jeferson/rasa-demo

<!-- ------------- -->

docker run -it --rm --user 1000 -v ${PWD}:/app rasa/rasa:3.0.8-full init --no-prompt
docker run --user 1000 -it -p 5005:5005 -v ${PWD}:/app rasa/rasa:3.0.8-full run --enable-api --cors "*"
docker-compose up
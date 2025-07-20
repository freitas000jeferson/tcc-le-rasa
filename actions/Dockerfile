FROM rasa/rasa-sdk:3.6.2  
# user root para instalação
USER root

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY actions.py /app/actions/actions.py

# Volta para o usuário padrão usado pelo Rasa SDK
USER 1001

CMD ["start", "--actions", "actions"]
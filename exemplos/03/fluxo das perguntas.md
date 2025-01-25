* iniciar
-inicia questionario by categoria
    traz 'qtd de perguntas'
    traz 'currentQuestionId'
    salva (inicia) 'qtd perguntas'
    salva (inicia) currentQuestionId
    salva (inicia) contador de perguntas
===========================
============ start loop ===
===========================
- busca pergunta by id
    salva id da 'pergunta 1'
    mostra 'pergunta 1'
* 'responde 1'
- busca resposta da pergunta by id
    traz 'qtd de perguntas restantes'
    traz resultado
    traz 'currentQuestionId'
    traz 'nextQuestionId'
    salva 'nextQuestionId' em 'currentQuestionId'
    salva 'contador de perguntas'+1
    verifica se é o fim do questionario
    mostra resultado
===========================
============ end loop =====
===========================

- finaliza questionario
    verifica se é o fim do questionario
    salva (None) 'qtd perguntas'
    salva (None) currentQuestionId
    salva (None) contador de perguntas
    mostra porcentagem de acertos

// adicionar posteriormente a continuação para o fluxo
// por enquanto finalizar conversação
- finaliza conversação
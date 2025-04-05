# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict

# from translate import Translator
import requests
import json
import asyncio


# SLOTS NAMES
ANSWER_QUESTION_ENTITY = 'answer_question_entity'
QUESTIONNARIE_ID_ENTITY= 'questionnarie_id_entity'   
CURRENT_QUESTION_ID_ENTITY = 'current_question_id_entity'
QUESTION_OPTIONS_ENTITY = 'question_options_entity'

USERNAME_ENTITY = 'username_entity'
COUNT_QUESTION_ENTITY = 'count_question_entity'
TOTAL_QUESTIONS_ENTITY = 'total_questions_entity'

GRAMMAR_CONTENT_ENTITY = 'grammar_content_entity'
VOCABULARY_CONTENT_ENTITY ="vocabulary_content_entity"

REQUESTED_SLOT = "requested_slot"

class ActionAskUsernameEntity(Action):

    def name(self) -> Text:
        return "action_ask_username_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender = tracker.sender_id
        username = tracker.get_slot(USERNAME_ENTITY)
        requested_slot = USERNAME_ENTITY
        if not username:
            response = httpGetProfile(sender)
            if 'data' in response:
                username = response["data"]['username']
                requested_slot= None
                # dispatcher.utter_message(response="utter_greet", username_entity=username)
            else:
                dispatcher.utter_message(response="utter_ask_username")
        
        return [SlotSet(USERNAME_ENTITY, username), SlotSet(REQUESTED_SLOT, requested_slot)]


# ##############################
# Action Gramatica
# ##############################

class ActionGetGrammar(Action):
    def name(self) -> Text:
        return "action_get_grammar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # user = "65f84c676f6d5a4ed8c1dc92"
        sender = tracker.sender_id
        category = tracker.get_slot(GRAMMAR_CONTENT_ENTITY)
        print('-------------------')
        print('Action Get Grammar')
        print("-------slots-------")
        print(sender, category)
        
        response = httpGetContent("GRAMMAR", category, sender )
        
        text_resp=""
        examples_resp=""
        json_resp = {'text': [], 'images': [], 'examples': []}

        for item in response:
            if item["text"]:
                json_resp["text"] += item["text"]
                text_resp += "\n\n".join(item["text"])+"\n\n"

            if item["examples"]:
                json_resp["examples"] += item["examples"]
                examples_resp+="\n\n".join(item["examples"])+"\n\n"
                
            if item["images"]:
                json_resp["images"] += item["images"]

        if examples_resp:
            text_resp+="\n\n"+examples_resp

        image_resp = None
        if len(response[0]["images"]) >0:
            image_resp = response[0]["images"][0]

        dispatcher.utter_message(text=text_resp, image=image_resp, json_message=json_resp)
        return []

# ##############################
# Action Vocabulario
# ##############################

class ActionGetVocabulary(Action):
    def name(self) -> Text:
        return "action_get_vocabulary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # user = "65f84c676f6d5a4ed8c1dc92"
        sender = tracker.sender_id
        print('-------------------')
        print('Action Get Vocabulary')
        print("-------slots-------")
        print(sender)
        
        response = httpGetContent("VOCABULARY", "None", sender )
        
        text_resp=""
        examples_resp=""
        json_resp = {'text': [], 'images': [], 'examples': []}

        for item in response:
            if item["text"]:
                json_resp["text"] += item["text"]
                text_resp += "\n\n".join(item["text"])+"\n\n"

            if item["examples"]:
                json_resp["examples"] += item["examples"]
                examples_resp+="\n\n".join(item["examples"])+"\n\n"
                
            if item["images"]:
                json_resp["images"] += item["images"]
        
        if examples_resp:
            text_resp+="\n\n"+examples_resp

        image_resp = None
        if len(response[0]["images"]) >0:
            image_resp = response[0]["images"][0]

        dispatcher.utter_message(text=text_resp, image=image_resp, json_message=json_resp)
        return []

# ##############################
# Validacao do Questionario
# ##############################
# faz a geração do quiz e traz a primeira pergunta
class ActionAskAnswerQuestionEntity(Action):
    def name(self) -> Text:
        return "action_ask_answer_question_entity"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict) -> List[Dict[Text, Any]]:
        print("# Buscar questionario")
        sender = tracker.sender_id
        category = tracker.get_slot(GRAMMAR_CONTENT_ENTITY)
        currentQuestionId = tracker.get_slot(CURRENT_QUESTION_ID_ENTITY)
        questionnarieId = tracker.get_slot(QUESTIONNARIE_ID_ENTITY)

        text_resp = None
        buttons_resp = None
        image_resp = None
        response = None
        options = None
        # nao sei se isso vai funcionar
        if not category:
            print("madou pegar o category")
            dispatcher.utter_message(response="utter_ask_grammar_content_entity")
        #---------------------

        if not currentQuestionId and not questionnarieId:
            # cria um novo questionario
            print("## Gerar questionario")
            response = httpGenerateQuiz(category, sender)
            
            questionnarieId = response["id"]
            currentQuestionId = response["question"]["id"]
        else:
            # busca a pergunta do questionario atual
            if not questionnarieId:
                response = httpGetCurrentQuestion(sender, None)
            else:
                response = httpGetCurrentQuestion(questionnarieId, currentQuestionId)
            print("## Buscar pergunta atual")
            # questionnarieId = response["id"]
            currentQuestionId = response["question"]["id"]
        
        if response["status"]== 'DONE':
            # Se o questionario ja foi finalizado
            return [
                SlotSet(REQUESTED_SLOT, None)
            ]
        print("Monta resposta")

        if response["question"]["image"]:
            image_resp = response["question"]["image"]
        if response["question"]["text"]:
            text_resp = "\n".join(response["question"]["text"])
        if response["question"]["options"]:
            buttons_resp = []
            options = []
            for item in response["question"]["options"]:
                payload = '/answer_question{"answer_question_entity":"'+item["text"]+'"}'
                buttons_resp.append({
                    "payload": payload, 
                    "title": item["text"]
                })
                options.append(item["text"].lower())
        
        dispatcher.utter_message(
            text=text_resp, 
            image= image_resp,
            buttons=buttons_resp,
            json_message= response
        )
        return [
            SlotSet(CURRENT_QUESTION_ID_ENTITY, str(currentQuestionId)),
            SlotSet(QUESTIONNARIE_ID_ENTITY, str(questionnarieId)),
            SlotSet(QUESTION_OPTIONS_ENTITY, options)
        ]

# faz o loop pra validar as respostas
class ValidateQuestionForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_question_form"

    def validate_grammar_content_entity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `grammar` value."""
        category = slot_value
        return {
            GRAMMAR_CONTENT_ENTITY: category
        }

    def validate_answer_question_entity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `answer` value."""
        print("## Responder pergunta")
        answer = slot_value
        sender = tracker.sender_id
        category = tracker.get_slot(GRAMMAR_CONTENT_ENTITY)
        currentQuestionId = tracker.get_slot(CURRENT_QUESTION_ID_ENTITY)
        questionnarieId = tracker.get_slot(QUESTIONNARIE_ID_ENTITY)
        options = tracker.get_slot(QUESTION_OPTIONS_ENTITY)

        # verifica se a resposta existe entre as opçoes
        if options and answer.lower() not in options:
            dispatcher.utter_message(text=f"The answer is one of the alternatives!")
            return { 
                ANSWER_QUESTION_ENTITY: None,
                GRAMMAR_CONTENT_ENTITY: category,
                QUESTIONNARIE_ID_ENTITY: questionnarieId,
                CURRENT_QUESTION_ID_ENTITY: currentQuestionId,
                QUESTION_OPTIONS_ENTITY: options
            }
        
        # responde pergunta
        response = httpAnswerQuestion(questionnarieId, currentQuestionId, answer, None)

        response_resp = None
        text_resp = None

        if response["lastQuestionStatus"]:
            if response["lastQuestionStatus"] == "RIGTH":
                response_resp="utter_right_answer"
            else:
                response_resp="utter_wrong_answer"
        
        dispatcher.utter_message(response=response_resp)

        # analiza se ja finalizou o questionario para continuar
        #  com o RULE(answer!=None) e mostrar o resultado
        # Se for response["status"] == DONE o quiz ta completo e permanece a resposta
        if response["status"] != "DONE":
            answer = None
            currentQuestionId = response["question"]["id"]
            
        return {
            ANSWER_QUESTION_ENTITY: answer,
            GRAMMAR_CONTENT_ENTITY: category,
            QUESTIONNARIE_ID_ENTITY: questionnarieId,
            CURRENT_QUESTION_ID_ENTITY: currentQuestionId,
            QUESTION_OPTIONS_ENTITY: options
        }


# Finalização do quiz mostrando o resultado
class ActionQuestionaryCompleted(Action):
    def name(self) -> Text:
        return "action_questions_completed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("## Dar resultado do quiz")
        # user = "65f84c676f6d5a4ed8c1dc92"
        sender = tracker.sender_id
        questionnarieId = tracker.get_slot(QUESTIONNARIE_ID_ENTITY)

        response = httpGetCurrentQuestion(questionnarieId, None)
        totalCorrectAnswers = response["totalCorrectAnswers"]
        totalQuestions = response["totalQuestions"]
        text_resp = ""
        if totalCorrectAnswers>= totalQuestions/2:
            text_resp="Congratulations!"
        else:
            text_resp="Keep trying!"

        text_resp += f'You answered {totalCorrectAnswers}/{totalQuestions} questions correctly'
        dispatcher.utter_message(text=text_resp)
        
        return [
            SlotSet(ANSWER_QUESTION_ENTITY, None),
            SlotSet(GRAMMAR_CONTENT_ENTITY, None),
            SlotSet(QUESTIONNARIE_ID_ENTITY, None),
            SlotSet(CURRENT_QUESTION_ID_ENTITY, None),
            SlotSet(QUESTION_OPTIONS_ENTITY, None),
        ]

# ##############################
# requests para o backend
# ##############################

BASE_URL = "http://192.168.3.4:3000/api/v1"
BASIC_AUTH = ("chatbotrasa","minhasenha1234")

def httpGetContent(typeContent, category, userId):
    userId = "65f84c676f6d5a4ed8c1dc92"
    url = BASE_URL+"/learn/"+ typeContent+"?category="+ category +"&userId=" + userId
    print(f"REQUEST: {url}")
    request = requests.get(url, auth = BASIC_AUTH)
    return request.json()

def httpGenerateQuiz(category, userId):
    # TODO: para testes modo interativo
    # userId = "65f84c676f6d5a4ed8c1dc92"
    url = BASE_URL+"/learn/questions"
    print(f"REQUEST: {url}")

    payload = {
        "category": category,
        "userId": userId
    }
    request = requests.post(url, data=payload, auth = BASIC_AUTH)
    return request.json()

def httpGetCurrentQuestion(questionnarieId, questionId):
    url = BASE_URL+"/learn/questions/"+questionnarieId
    if questionId:
        url+= "?questionId="+ questionId 
    print(f"REQUEST: {url}")
    request = requests.get(url, auth = BASIC_AUTH)
    return request.json()

def httpAnswerQuestion(questionnarieId, questionId, answer, answerId):
    url = BASE_URL+"/learn/questions/"+questionnarieId
    print(f"REQUEST: {url}")
    payload = {
        "questionId": questionId,
        "answer": answer,
        "answerId": answerId
    }
    request = requests.post(url, data=payload, auth = BASIC_AUTH)
    return request.json()

def httpGetProfile(userId):
    # TODO: para testes modo interativo
    # userId = "65f84c676f6d5a4ed8c1dc92"
    url = BASE_URL+'/users/'+userId+'/profile'
    print(f"REQUEST: {url}")
    request = requests.get(url,auth = BASIC_AUTH)
    return request.json()
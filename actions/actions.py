# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet

# from translate import Translator
import requests
import json
import asyncio

BASE_URL = "http://localhost:3000/api/v1"

BASIC_AUTH = ("chatbotrasa","minhasenha1234")

# SLOTS NAMES
ANSWER_QUESTION_ENTITY = 'answer_question_entity'
COUNT_QUESTION_ENTITY = 'count_question_entity'
CURRENT_QUESTION_ID_ENTITY = 'current_question_id_entity'
GRAMMAR_CONTENT_ENTITY= 'grammar_content_entity'


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

# ##############################
# requests para o backend
# ##############################

def httpGetContent(typeContent, category, userId):
    url = BASE_URL+"/learn/"+ typeContent +"?category="+ category + "&userId="+userId 
    request = requests.get(url, auth = BASIC_AUTH)
    return request.json()


def httpGenerateQuiz(category, userId):
    url = BASE_URL+"/learn/questions"
    payload = {
        "category": category,
        "userId": userId
    }
    request = requests.post(url, data=payload, auth = BASIC_AUTH)
    return request.json()

def httpAnswerQuestion(questionnarieId, questionId, answer, answerId):
    url = BASE_URL+"/learn/questions/"+questionnarieId
    payload = {
        "questionId": questionId,
        "answer": answer,
        "answerId": answerId
    }
    request = requests.post(url, data=payload, auth = BASIC_AUTH)
    return request.json()
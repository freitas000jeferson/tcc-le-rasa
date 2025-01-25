# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests
import asyncio
from translate import Translator
from typing import Any, Text, Dict, List

 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
  

baseUrl = "https://localhost:3000/api/v1"

class ActionTranslate(Action):
    def name(self) -> Text:
        return "action_translate"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message ['entities']
        word = ""
        form = "pt_to_en"
        for entity in entities:
            if entity["entity"]== "form_of_translation_entity":
                form = entity["value"]
            elif entity["entity"]== "translate_word_entity": 
                word = entity["value"] 
        
        if(form == 'pt_to_en'):
            t =  Translator(from_lang= "portuguese", to_lang="english")
        elif(form == 'en_to_pt'):
            t =  Translator(from_lang= "english", to_lang="portuguese")
        else:
            t =  Translator(from_lang= "portuguese", to_lang="english")
        result = t.translate(word)
        print(result)
        print (entities)
        dispatcher.utter_message(text=f"the translation is {result.upper()}")
        
        # result = t.translate("{word}")
        # dispatcher.utter_message(text=f"{result}")
        print("FINAL - action_translate ------------------------------")
        return [ ]

class ActionGetQuestion(Action):

    def name(self) -> Text:
        return "action_get_question"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender = tracker.sender_id
        entities = tracker.latest_message['entities']        
        values=""
        print("sender", sender)
        for entity in entities:
            print(entity["entity"], entity["value"])
        print("----------")

        # response = await findQuestion(sender, question_category)
        # dispatcher.utter_message(
        #     text=f"{response['body_text']}",
        #     buttons=response['body_buttons'],
        #     image=f"{response['body_image']}")

        return [
            # SlotSet("question_category_entity", None), 
                # SlotSet("question_id_entity", response['id']),
                # SlotSet("answer_question_entity", None)
                ]
        

class ActionAnswerQuestion(Action):

    def name(self) -> Text:
        return "action_answer_question"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender = tracker.sender_id
        answer_selected = tracker.get_slot("answer_question_entity")
        question_id = tracker.get_slot("question_id_entity")


        # response = await answerQuestion(sender,question_id, answer_selected)

        return [
            # SlotSet("question_category_entity", None),
            # SlotSet("question_id_entity", None),
            # SlotSet("answer_question_entity", None)
            ]



async def findQuestion(sender, category):
    url = baseUrl+'/question/' 
    myobj = {
        "user": sender,
        "category": category,
    }
    response = await requests.post(url, json = myobj)
    return response

async def answerQuestion(sender, question_id, answer):
    url = baseUrl+'/question/answer' 
    myobj = {
        "user": sender,
        "questionId": question_id,
        "answer": answer
    }
    response = await requests.post(url, json = myobj)
    return response

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

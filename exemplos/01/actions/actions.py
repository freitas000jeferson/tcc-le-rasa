# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import random

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher

CURRENT_QUESTION_ID_ENTITY = 'current_question_id_entity'
COUNT_QUESTION_ENTITY = 'count_question_entity'
ANSWER_QUESTION_ENTITY = 'answer_question_entity'

QUESTIONS = [{
        "text": "questão 00",
        "ans":  "am",
        "buttons": [
            {"title": "am", "payload":'/answer_question{"answer_question_entity":"am"}'},
            {"title": "is", "payload":'/answer_question{"answer_question_entity":"is"}'},
            {"title": "are", "payload":'/answer_question{"answer_question_entity":"are"}'}, 
        ],
    },
    # {
    #     "text": "questão 01",
    #     "ans":  "am",
    #     "buttons": [
    #         {"title": "am", "payload":'/answer_question{"answer_question_entity":"am"}'},
    #         {"title": "is", "payload":'/answer_question{"answer_question_entity":"is"}'},
    #         {"title": "are", "payload":'/answer_question{"answer_question_entity":"are"}'}, 
    #     ],
    # },
    # {
    #     "text": "questão 02",
    #     "ans":  "is",
    #     "buttons": [
    #         {"title": "am", "payload":'/answer_question{"answer_question_entity":"am"}'},
    #         {"title": "is", "payload":'/answer_question{"answer_question_entity":"is"}'},
    #         {"title": "are", "payload":'/answer_question{"answer_question_entity":"are"}'}, 
    #     ]
    # },
    # {
    #     "text": "questão 03",
    #     "ans":  "are",
    #     "buttons": [
    #         {"title": "am", "payload":'/answer_question{"answer_question_entity":"am"}'},
    #         {"title": "is", "payload":'/answer_question{"answer_question_entity":"is"}'},
    #         {"title": "are", "payload":'/answer_question{"answer_question_entity":"are"}'}, 
    #     ]
    # },
    
    # {
    #     "text": "questão 04",
    #     "ans":  "is",
    #     "buttons": [
    #         {"title": "am", "payload":'/answer_question{"answer_question_entity":"am"}'},
    #         {"title": "is", "payload":'/answer_question{"answer_question_entity":"is"}'},
    #         {"title": "are", "payload":'/answer_question{"answer_question_entity":"are"}'}, 
    #     ]
    # },
    # {
    #     "text": "questão 05",
    #     "ans":  "are",
    #     "buttons": [
    #         {"title": "am", "payload":'/answer_question{"answer_question_entity":"am"}'},
    #         {"title": "is", "payload":'/answer_question{"answer_question_entity":"is"}'},
    #         {"title": "are", "payload":'/answer_question{"answer_question_entity":"are"}'}, 
    #     ]
    # },
]
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionQuestionsAccepteds(Action):

    def name(self) -> Text:
        return "action_questions_accepteds"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        countQuestionAccepts = tracker.get_slot(COUNT_QUESTION_ENTITY)

        dispatcher.utter_message(text=f"You are aceppted ({countQuestionAccepts}/{len(QUESTIONS)}) questions!")

        return []

class ActionAskAnswerQuestionEntity(Action):
    def name(self) -> Text:
        return "action_ask_answer_question_entity"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        id = tracker.get_slot(CURRENT_QUESTION_ID_ENTITY)
        currentQuestionId = 0 
        if id != None: currentQuestionId = int(id)

        element = QUESTIONS[currentQuestionId]
        print(f"# ID_QUESTION: {currentQuestionId} ################################")
        dispatcher.utter_message(
            text=f"{element['text']}",
            buttons=[{"title": item["title"], "payload":item["payload"]} for item in element["buttons"]],
        )
        return [SlotSet(CURRENT_QUESTION_ID_ENTITY, str(currentQuestionId))]

class ValidateQuestionForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_question_form"

    def validate_answer_question_entity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `question` value."""
        print(f'# question: {slot_value}')
        currentQuestionIdAux = tracker.get_slot(CURRENT_QUESTION_ID_ENTITY)
        currentQuestionId = int(currentQuestionIdAux)
        countQuestionAccepts = tracker.get_slot(COUNT_QUESTION_ENTITY)

        element = QUESTIONS[currentQuestionId]
        options = [i["title"] for i in element["buttons"]]
        print(slot_value, options)
        print("Esta nas opções:",slot_value not in options)
        if slot_value not in options:
            print("Repetiu a pergunta")
            dispatcher.utter_message(text=f"The answer is one of the alternatives!")
            return {ANSWER_QUESTION_ENTITY: None}
        
        # valida a resposta do back
        isCorrect = answerQuestion(currentQuestionId, slot_value)
        if isCorrect:
            print("Resposta correta")
            countQuestionAccepts+=1
        print(isCorrect, slot_value)
        
        # pega proxima questão
        currentQuestionId+=1
        if len(QUESTIONS) > currentQuestionId:
            print("Proxima pergunta")
            return {
                ANSWER_QUESTION_ENTITY: None, 
                CURRENT_QUESTION_ID_ENTITY: str(currentQuestionId), 
                COUNT_QUESTION_ENTITY: countQuestionAccepts
            }

        print("Finalizando")
        return {
            ANSWER_QUESTION_ENTITY: "Finalizando", 
            CURRENT_QUESTION_ID_ENTITY: str(currentQuestionId), 
            COUNT_QUESTION_ENTITY: countQuestionAccepts
        }

def answerQuestion(id, ans):
    question = QUESTIONS[id]
    return question["ans"] == ans

class ValidateLearningForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_learning_form"

    def validate_learning_content_entity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `learning_content_entity` value."""
        print(f'# content: {slot_value}')
        # return {"learning_content_entity", slot_value}
        return {}
    
    def validate_learning_method_entity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `learning_method_entity` value."""
        print(f'# method: {slot_value}')

        # return {"learning_method_entity", slot_value}
        return {}


        
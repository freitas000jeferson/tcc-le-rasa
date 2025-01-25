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

ANSWER_QUESTION_ENTITY = "answer_question_entity"
COUNT_QUESTION_ENTITY = "count_question_entity"
CURRENT_QUESTION_ID_ENTITY = "current_question_id_entity"
GRAMMAR_CONTENT_ENTITY = "grammar_content_entity"
VOCABULARY_CONTENT_ENTITY = "vocabulary_content_entity"




class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

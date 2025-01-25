from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
from translate import Translator
import requests
import json
import asyncio

baseUrl = "http://localhost:3000/api/v1"

# SLOTS NAMES
LEARNING_METHOD_ENTITY = 'learning_method_entity'
LEARNING_CONTENT_ENTITY = 'learning_content_entity'
CURRENT_QUESTION_ID_ENTITY = 'current_question_id_entity'
ANSWER_QUESTION_ENTITY = 'answer_question_entity'
COUNT_QUESTION_ENTITY = 'count_question_entity'
QTD_QUESTIONS_ENTITY = 'qtd_questions_entity'
FINISHING_QUESTIONS_ENTITY = 'finishing_questions_entity'



class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionJoke(Action):
    def name(self):
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        response = findQuestion("", "")
        print(response)
        dispatcher.utter_message(text=response['bodyText'],
                                buttons=response['bodyButtons'], 
                                image=response['bodyImage'])
        # request = requests.get('http://api.icndb.com/jokes/random').json()  # make an api call
        # joke = request['value']['joke']  # extract a joke from returned json response
        # dispatcher.utter_message(text=joke, buttons=[
        #         {"payload": '/response{"responses_questions": "none"}', "title": "none"},
        #         {"payload":'/response{"responses_questions": "none"}', "title": "none"},
        #         {"payload": '/response{"responses_questions": "none"}', "title": "none"}
        #     ] )  # send the message back to the user
        return []

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

# ===========================
# ======== content ==========
# ===========================

class ActionGetContent(Action):

    def name(self) -> Text:
        return "action_get_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender = tracker.sender_id
        content = tracker.get_slot(LEARNING_CONTENT_ENTITY)
        method = tracker.get_slot(LEARNING_METHOD_ENTITY)
        response = getContent(sender, content, method)
        print('\nActionGetContent')

        print("-----slots-----")
        print("content", content)
        print("method", method) 

        print("-----answer-----")
        print (response)
        print("----------")
        print("----------")
        
        dispatcher.utter_message(text=f"conteudo...{response.get('bodyText')} -{content} {method} !!!!!!",)
    
        return []
# ===========================
# ======== questions ========
# ===========================

class ActionInitQuestions(Action):

    def name(self) -> Text:
        return "action_init_questions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender = tracker.sender_id
        content = tracker.get_slot(LEARNING_CONTENT_ENTITY)
        
        response = initQuestionsRequest(sender, content)
        print('\nActionInitQuestions')

        print("-----slots-----")
        print('content: ', content)

        print("-----initQuestion-----")
        print (response)
        print("----------")
        
        qtdQuestions = response.get("qtdQuestions")
        currentQuestionId = response.get("currentQuestionId")
        
        return [
            SlotSet(QTD_QUESTIONS_ENTITY, qtdQuestions),
            SlotSet(CURRENT_QUESTION_ID_ENTITY, currentQuestionId),
            SlotSet(COUNT_QUESTION_ENTITY, 0),
            SlotSet(FINISHING_QUESTIONS_ENTITY, False)
            ]

class ActionGetQuestion(Action):

    def name(self) -> Text:
        return "action_get_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender = tracker.sender_id
        currentQuestionId = tracker.get_slot(CURRENT_QUESTION_ID_ENTITY)
        
        response = findQuestionById(sender, currentQuestionId)
        bodyText = response.get("bodyText")
        bodyImages = response.get("bodyImage")
        bodyButtons = response.get('bodyButtons')
        print('\nActionGetQuestion')
        print("-----slots-----")
        print('currentQuestionId: ', currentQuestionId)

        print("-----question-----")
        print (response)
        print("----------")

        if bodyImages!=None and len(bodyImages)>0:
            print ("ActionGetQuestion -> [1]")
            for id in range(len(bodyImages)):
                dispatcher.utter_message(image=f"{bodyImages[id]}")

        if (bodyText!=None and len(bodyText)>0) and (bodyButtons!=None and len(bodyButtons)>0):
            print ("ActionGetQuestion -> [2]")
            
            if len(bodyText)>=2:
                for id in range(len(bodyText)-1):
                    dispatcher.utter_message(text=f"{bodyText[id]}")
            dispatcher.utter_message(
                text = f"{bodyText[-1]}",
                buttons = bodyButtons)

        elif (bodyText!=None and len(bodyText)>0) and (bodyButtons==None or len(bodyButtons)==0):
            print ("ActionGetQuestion -> [3]")  
            for id in range(len(bodyText)):
                dispatcher.utter_message(text=f"{bodyText[id]}")

        elif (bodyText==None or len(bodyText)==0) and (bodyButtons!=None and len(bodyButtons)>0):
            print ("ActionGetQuestion -> [4]")
            dispatcher.utter_message(
                buttons = bodyButtons)   


        return []

class ActionAnswerQuestion(Action):

    def name(self) -> Text:
        return "action_answer_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender = tracker.sender_id

        currentQuestionId = tracker.get_slot(CURRENT_QUESTION_ID_ENTITY)
        answer = tracker.get_slot(ANSWER_QUESTION_ENTITY)
        countQuestions = tracker.get_slot(COUNT_QUESTION_ENTITY)
        finishing = tracker.get_slot(FINISHING_QUESTIONS_ENTITY)

        response = answerQuestionById(sender, currentQuestionId, answer)
        print('\nActionAnswerQuestion')
        print("-----slots-----")
        print('currentQuestionId: ', currentQuestionId)
        print('answer: ', answer)
        print('countQuestions: ', countQuestions)
        print('finishing: ', finishing)

        print("-----answer-----")
        print (response)
        print("----------")
        nextQuestionId = response.get("nextQuestionId")
        result = response.get("result")
        qtdQuestions = response.get("qtdQuestions")
        rightAnswer = response.get("answerText") 
        
        countQuestions=countQuestions+1
        if result:
            dispatcher.utter_message(text=f"very well, it is correct")
        else: 
            dispatcher.utter_message(text=f"it's wrong :(")
        
        # testar se lança para proxima questão    
        if qtdQuestions <= countQuestions:
            print("FINALIZOU")
            finishing= True
            dispatcher.utter(response = "utter_goodbye")

        return [
            SlotSet(QTD_QUESTIONS_ENTITY, qtdQuestions),
            SlotSet(CURRENT_QUESTION_ID_ENTITY, nextQuestionId),
            SlotSet(COUNT_QUESTION_ENTITY, countQuestions),
            SlotSet(FINISHING_QUESTIONS_ENTITY, finishing)
            ]

class ActionFinalizeQuestion(Action):

    def name(self) -> Text:
        return "action_finalize_questions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender = tracker.sender_id

        response = finalizeQuestions(sender)
        print('\nActionFinalizeQuestion')

        print("-----finishing-----")
        print (response)
        print("----------")
        porcentRightQuestions = response.get("porcentRightQuestions")
        value = porcentRightQuestions*100
        dispatcher.utter_message(text=f"you got {value}% of the questions right")

        if value>=70:
            dispatcher.utter_message(text=f"you are doing very well, keep it up")
        else: 
            dispatcher.utter_message(text=f"just a little... try moving the content later to improve")
        
        return [
            SlotSet(QTD_QUESTIONS_ENTITY, None),
            SlotSet(CURRENT_QUESTION_ID_ENTITY, None),
            SlotSet(COUNT_QUESTION_ENTITY, None),
            SlotSet(FINISHING_QUESTIONS_ENTITY, None)
            ]

# ===========================
# ======= requests ==========
# ===========================
def getContent(sender, content, method):
    response = {
        '_id': '620d961b486c46860111ed3e',
        'bodyText': ['Um texto enviado'],
        'bodyImage': ['imagem'],
        'bodyButtons': [],
        'bodyExamples': [],
        'category': 'TO_BE',
        'level': 1,
        'createdAt': '2022-02-17T00:11:38.222Z',
    }
    return response

qtd=3
def initQuestionsRequest(sender, category):
    # TODO: aqui fica a request pra api
    response = {
        "qtdQuestions": qtd,
        "currentQuestionId": '1',
        "questions": ['1','11','111']
    }
    return response

def findQuestionById(sender, questionId):
    # TODO: aqui fica a request pra api
    response = {
        "id": questionId,
        "bodyText": ["question"],
        "bodyButtons": [
            {
                "title": 'am', 
                "payload": '/answer_question{"answer_question_entity":"am"}',
            },
            {
                "title": 'are', 
                "payload": '/answer_question{"answer_question_entity":"are"}',
            }
        ],
        "answerText": 'b',
        "answerOption": 1,
        "categoryId": 'any'
    }
    return response

def answerQuestionById(sender, questionId, answer):
    # TODO: aqui fica a request pra api
    response ={
        "id": questionId,
        "bodyText": ["question"],
        "bodyButtons": [
            {
                "title": 'am', 
                "payload": '/answer_question{"answer_question_entity":"am"}',
            },
            {
                "title": 'are', 
                "payload": '/answer_question{"answer_question_entity":"are"}',
            }
        ],
        "result": answer=='are',
        "answerText": 'are',
        "answerOption": 1,
        "nextQuestionId": f'1{questionId}',
        "qtdQuestions": qtd
    }
    return response

def finalizeQuestions(sender):
    # TODO: aqui fica a request pra api
    response = {
        "porcentRightQuestions": 0.7
    }
    return response
# ===========================
# ===========================
# ===========================

def findQuestion(sender, category):
    # url = baseUrl+'/question/random' 
    url = baseUrl+'/hc/message'
    myobj = {
        # "user": sender,
        # "category": category,
    }
    return requests.post(url, json = myobj).json()
    

async def answerQuestion(sender, question_id, answer):
    url = baseUrl+'/question/answer' 
    myobj = {
        "user": sender,
        "questionId": question_id,
        "answer": answer
    }
    response = await requests.post(url, json = myobj)
    return response

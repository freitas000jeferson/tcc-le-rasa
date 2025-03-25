print("INIT")
import requests
import json
import asyncio
BASE_URL = "http://localhost:3000/api/v1"
BASIC_AUTH = ("chatbotrasa","minhasenha1234")
def httpGetContent(typeContent, category, userId):
    url = BASE_URL+'/learn/'+ typeContent +"?category="+ category + "&userId="+userId 
    request = requests.get(url, auth = BASIC_AUTH)
    return request.json()

def httpGenerateQuiz(category, userId):
    url = BASE_URL+'/learn/questions'
    payload = {
        "category": category,
        "userId": userId
    }
    request = requests.post(url, data=payload, auth = BASIC_AUTH)
    return request.json()


def httpAnswerQuestion(questionnarieId, questionId, answer, answerId):
    url = BASE_URL+'/learn/questions/'+questionnarieId
    payload = {
        "questionId": questionId,
        "answer": answer,
        "answerId": answerId
    }
    request = requests.post(url, data=payload, auth = BASIC_AUTH)
    return request.json()

resp = httpAnswerQuestion("67d47ad337eb8711ca1f3713","675defbad53f131231833d8d","in", None )

print("resp:", resp)
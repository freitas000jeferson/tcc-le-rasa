print("INIT")
# import requests
# import json
# import asyncio
# BASE_URL = "http://192.168.3.4:3000/api/v1"
# BASIC_AUTH = ("chatbotrasa","minhasenha1234")
# def httpGetContent(typeContent, category, userId):
#     url = BASE_URL+'/learn/'+ typeContent +"?category="+ category + "&userId="+userId 
#     request = requests.get(url, auth = BASIC_AUTH)
#     return request.json()

# def httpGenerateQuiz(category, userId):
#     url = BASE_URL+'/learn/questions'
#     payload = {
#         "category": category,
#         "userId": userId
#     }
#     request = requests.post(url, data=payload, auth = BASIC_AUTH)
#     return request.json()


# def httpAnswerQuestion(questionnarieId, questionId, answer, answerId):
    # url = BASE_URL+'/learn/questions/'+questionnarieId
    # payload = {
    #     "questionId": questionId,
    #     "answer": answer,
    #     "answerId": answerId
    # }
    # request = requests.post(url, data=payload, auth = BASIC_AUTH)
    # return request.json()

# resp = httpAnswerQuestion("67d47ad337eb8711ca1f3713","675defbad53f131231833d8d","in", None )
# resp = httpGetContent("GRAMMAR", "preposition", "65f84c676f6d5a4ed8c1dc92")
# print("resp:", resp)
resp = [{'text': ['[Teste][GRAMMAR] Texto 0', 'atavus tepidus apparatus tabula impedit commemoro'], 'images': ['https://picsum.photos/seed/BciXJwfM/408/2167'], 'examples': []}]
response = {
    "id": "67d4633ad71e25b974f54606",
    "status": "TO_DO",
    "totalQuestions": 3,
    "totalCorrectAnswers": 0,
    "question": {
        "id": "675defb9d53f131231833d81",
        "text": [
            "My dog ___ playing in the garden."
        ],
        "image": "",
        "options": [
            {
                "id": 0,
                "text": "am"
            },
            {
                "id": 1,
                "text": "is"
            },
            {
                "id": 2,
                "text": "are"
            }
        ],
        "status": "TO_DO"
    }
}
buttons_resp=None
if response["question"]["options"]:
    buttons_resp = []
    for item in response["question"]["options"]:
        payload = '/answer_question{"answer_question_entity":"'+item["text"]+'"}'
        buttons_resp.append({
            "payload": payload, 
            "title": item["text"]
        })
    
print(buttons_resp)
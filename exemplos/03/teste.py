import requests
import json

def run():
    response = a()
    if len(response["body_text"])>2:
        for id in range(len(response["body_text"])-1):
            print('-> ',response["body_text"][id])
        
    print(response["body_text"][-1])

def req():
    response = requests.get('https://www.thunderclient.com/welcome',)

    return response.json()
def a():
    response = {
        "body_text": ["2","1","231","qwe"],
    }
    return response

run()
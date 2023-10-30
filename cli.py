from melba import Melba

import json, time

wss = False
host = "127.0.0.1"
port = 9877
endpoint = "/llm"

melba = Melba()


def process_request(request):
    return {"response_text": response_text}


if __name__ == "__main__":
    person = "chatter"
    while True:
        message = input("Message: ")
        response_text = melba.get_response(message, person)
        print("Response:")
        print(response_text)

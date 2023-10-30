from melba import Melba

import json, traceback, time
import websockets.sync.client

wss = False
host = "127.0.0.1"
port = 9877
endpoint = "/llm"

melba = Melba()


def process_request(request):
    response_text = melba.get_response(request["message"], request["person"])
    return {"response_text": response_text}


if __name__ == "__main__":
    while True:
        connection_url = f"{'wss' if wss else 'ws'}://{host}:{port}{endpoint}"
        print(f"Connecting to backend at {connection_url}")
        try:
            with websockets.sync.client.connect(connection_url) as websocket:
                while True:
                    request = json.loads(websocket.recv())
                    print(request)
                    response = process_request(request)
                    websocket.send(json.dumps(response))
        except Exception as e:
            print("Exception during WebSocket connection:")
            print(traceback.format_exc())
        print(f"Connection to backend lost, retrying in 3s")
        time.sleep(3)

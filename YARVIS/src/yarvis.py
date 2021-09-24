import time
import wave 
from threading import Thread
import json
import requests
import sys

from speaker import YarvisSpeaker
from listener import YarvisListener

from flask import Flask, request

'''
Defining Global Variables
'''

# Status:
# False: stand by
# True: listening

status = False

yarvis_speaker = YarvisSpeaker()
yarvis_listener = YarvisListener(max_time_listening=10)
url = "http://localhost:5000/execute_command"

def listen_command():
    yarvis_listener.listen()
    yarvis_listener.analyze_audio()
    data_ = {'query':yarvis_listener.get_text()}
    res = requests.post(url,data=json.dumps(data_))
    if res:
        yarvis_speaker.saidit(res.text)

def command_action():
    global status
    if not status:
        command_thread = Thread(target=listen_command)
        command_thread.start()
    else :
        yarvis_listener.stop_listening()
    status = not status


app = Flask(__name__)

@app.route("/",methods=["POST"])
def wakeup():
    try:
        if request.method == "POST":
            data_ = eval(request.get_data())
            if "query" in data_:
                command_action()
            return "success"
        else:
            return "error"
    except:
        print("something went wrong with the request")

if __name__ == "__main__":
    app.run(port=5001)

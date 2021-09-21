import time
import wave 
from threading import Thread
import json
import requests

import pyaudio
import speech_recognition as sr
from speaker import YarvisSpeaker
from listener import YarvisListener

ys = YarvisSpeaker()
yl = YarvisListener(max_time_listening=10)
url = "http://localhost:5000/execute_command"

def enter_command():
    yl.listen()
    yl.analyze_audio()
    data_ = {'query':yl.get_text()}
    res = requests.post(url,data=json.dumps(data_))
    if res:
        ys.saidit(res.text)


command_thread = Thread(target=enter_command)
command_thread.start()

opt = ""
while True:
    opt = input()
    if opt == "a":
        yl.listening = False
        break
    elif opt == "b":
        print(len(yl.curr_frame))

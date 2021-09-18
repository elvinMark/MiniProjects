import pyaudio
import speech_recognition as sr
import wave 
from speaker import YarvisSpeaker
from listener import YarvisListener
import time
from threading import Thread


ys = YarvisSpeaker()
yl = YarvisListener(max_time_listening=10)

def enter_command():
    yl.listen()
    yl.analyze_audio()
    ys.saidit(yl.get_text())

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

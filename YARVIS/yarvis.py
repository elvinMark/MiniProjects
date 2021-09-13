import pyaudio
import speech_recognition as sr
import wave 
from speaker import YarvisSpeaker
from listener import YarvisListener
import time

# ys = YarvisSpeaker()

# ys.start()

# print("starting")
# time.sleep(1)
# ys.enqueue("Hello")
# ys.enqueue("Test")
# print("Waiting")
# time.sleep(3)
# ys.closing()

yl = YarvisListener()

yl.start()

for i in range(5):
    time.sleep(1)
    print(yl.get_text())
    time.sleep(1)

yl.closing()

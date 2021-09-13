from gtts import gTTS
import os
from threading import Thread
import time

class YarvisSpeaker(Thread):
    def __init__(self):
        super().__init__()
        self.buffer = []
        self.running = True
        
    def saidit(self,sentence):
        tmp_ = gTTS(sentence,lang="en",slow=False)
        tmp_.save("tmp.mp3")
        os.system("mpg123 tmp.mp3")

    def enqueue(self,sentence):
        self.buffer.append(sentence)

    def closing(self):
        self.running = False
    
    def run(self):
        while self.running:
            if self.buffer:
                sentence = self.buffer.pop(0)
                self.saidit(sentence)
            else:
                time.sleep(1)
        print("Speaker Finished!")

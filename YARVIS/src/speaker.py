from gtts import gTTS
import os

class YarvisSpeaker:
    def __init__(self):
        pass
        
    def saidit(self,sentence):
        tmp_ = gTTS(sentence,lang="en",slow=False)
        tmp_.save("tmp.mp3")
        os.system("mpg123 tmp.mp3")

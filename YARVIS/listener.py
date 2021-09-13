import pyaudio
import speech_recognition as sr
from threading import Thread
import time

class SpeechRecognition:
    def __init__(self):
        self.recog_helper = sr.Recognizer()

    def get_text(self,frame_data,rate,sample_width):
        audio_data = sr.AudioData(frame_data,rate,sample_width)
        info = self.recog_helper.recognize_google(audio_data,show_all=True)
        if info:
            return info["alternative"][0]["transcript"]
        else:
            return None

class YarvisSpeechRecognition(Thread):
    def __init__(self,rate,sample_width):
        super().__init__()
        self.rate = rate
        self.sample_width = sample_width
        self.running = True
        self.speech_buffer = []
        self.text_buffer = []

    def enqueue(self,frame_data):
        self.speech_buffer.append(frame_data)
    
    def get_text(self):
        if self.text_buffer:
            return self.text_buffer.pop(0)
        return None

    def closing(self):
        self.running = False
    
    def run(self):
        recog = SpeechRecognition()
        while self.running:
            if self.speech_buffer:
                frame_data = self.speech_buffer.pop(0)
                info = recog.get_text(frame_data,self.rate,self.sample_width)
                if info:
                    self.text_buffer.append(info)
            else:
                time.sleep(1)
        print("Closing Speech Recognition")

class YarvisListener(Thread):
    def __init__(self,rate=16000,channels=1,chunk=1000,format=pyaudio.paInt16,sample_width=2):
        super().__init__()
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.format = format
        self.sample_width = sample_width
        self.buffer = []
        self.running = True

    def get_text(self):
        if self.buffer:
            return self.buffer.pop(0)
        return None
    
    def closing(self):
        self.running = False
    
    def run(self):
        audio = pyaudio.PyAudio()
        recog = YarvisSpeechRecognition(self.rate,self.sample_width)
        stream = audio.open(self.rate,self.channels,self.format,input=True,frames_per_buffer=self.chunk)
        frames = []
        recog.start()
        while self.running:
            for i in range(0,self.rate // self.chunk):
                frames.append(stream.read(self.chunk))

            recog.enqueue(b"".join(frames))
            frames = []
            text_ = recog.get_text()
            if text_:
                self.buffer.append(text_)
        recog.closing()
        print("Closing Listener")

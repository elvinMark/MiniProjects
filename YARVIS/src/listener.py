import pyaudio
import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recog_helper = sr.Recognizer()

    def get_text(self,frame_data,rate,sample_width):
        audio_data = sr.AudioData(frame_data,rate,sample_width)
        info = self.recog_helper.recognize_google(audio_data,show_all=True)
        if info:
            return info["alternative"][0]["transcript"]
        else:
            return None

class YarvisListener:
    def __init__(self,rate=16000,channels=1,chunk=1000,format=pyaudio.paInt16,sample_width=2,max_time_listening=10):
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.format = format
        self.sample_width = sample_width
        self.max_time_listening = max_time_listening
        self.listening = True
        self.curr_frame = None
        self.frames = []
        self.recognizer = SpeechRecognizer()
        self.text_ = None
        
    def listen(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(self.rate,self.channels,self.format,input=True,frames_per_buffer=self.chunk)
        self.frames = []
        self.text_ = None
        for i in range(int(self.max_time_listening* self.rate/self.chunk)):
            self.curr_frame = stream.read(self.chunk)
            self.frames.append(self.curr_frame)
            if not self.listening:
                break
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
    def analyze_audio(self):
        self.text_ =  self.recognizer.get_text(b"".join(self.frames),self.rate,self.sample_width)

    def get_text(self):
        return self.text_

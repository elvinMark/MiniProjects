import pyaudio
import speech_recognition as sr
import wave 

opt = 2

###=========Getting data from wav file============###
if opt == 1:
    t = wave.open("tmp.wav","rb")

    audio_data = sr.AudioData(t.readframes(-1),t.getframerate(),t.getsampwidth())
#    print(audio_data.frame_data)
    recog = sr.Recognizer()

    info = recog.recognize_google(audio_data)


###=========Getting data from mic and pyaudio========###

elif opt == 2:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1000
    RECORD_SECONDS = 2


    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)

    frames = []

    print("start mic")

    for i in range(0,int(RATE/CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("finishing mic")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    data_ = b"".join(frames)
    # this time sample width is 2 because we are using 16bits (2bytes)
    # as it can be seen int the format
    audio_data = sr.AudioData(data_,RATE,2)

    recog = sr.Recognizer()
    print(recog.recognize_google(audio_data,show_all=True))


else:
    print("choose a valid option")

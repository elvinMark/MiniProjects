import numpy as np 
import neural as nn 
import json 
import sys
import time
import random
import speech_recognition as sr
from gtts import gTTS
import os

weather = ["sunny","rainy","cloudy","snowy","windy"]

wkday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

r = sr.Recognizer()
mic = sr.Microphone()

def get_speech():
    info = []
    while not info:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        info = r.recognize_google(audio,show_all=True)
        if info:
            break
        print("Can you repeat please")
    return info["alternative"][0]["transcript"]

if __name__ == "__main__":
    with open("intentions.json") as f:
        data = json.load(f)

    tags = []
    words = []
    for tag in data["tags"]:
        tags.append(tag)
        for s in data["tags"][tag]["phrases"]:
            for word in s.lower().split():
                if word not in words:
                    words.append(word)
        
    in_data = []
    out_data = []
    
    for i in range(len(tags)):
        tmp_out = np.zeros(len(tags))
        tmp_out[i] = 1
        for s in data["tags"][tags[i]]["phrases"]:
            tmp_in = np.zeros(len(words))
            for word in s.lower().split():
                tmp_in[words.index(word)] = 1
            in_data.append(tmp_in)
            out_data.append(tmp_out)
        
    in_data = np.array(in_data)
    out_data = np.array(out_data)
    
    if sys.argv[1] == "training":
        model = []
        model.append(nn.fcc(len(words),10,fun_type="sigmoid"))
        model.append(nn.fcc(10,10,fun_type="leaky_relu"))
        model.append(nn.fcc_softmax(10,len(tags),fun_type="leaky_relu"))
        nn.train(model,in_data,out_data,alpha=0.1)
        nn.save_model(model,"data.dat")
        print(nn.forward(model,in_data))
    elif sys.argv[1] == "test":
        model = []
        model.append(nn.fcc(len(words),10,fun_type="sigmoid"))
        model.append(nn.fcc(10,10,fun_type="leaky_relu"))
        model.append(nn.fcc_softmax(10,len(tags),fun_type="leaky_relu"))
        nn.load_model(model,"data.dat")
        #print(nn.forward(model,in_data))
        inp = ""
        while inp != "exit":
            # Text Input
            # inp = input("Input:\n")
            # Speech input
            inp = get_speech()
            test_in = np.zeros((1,len(words)))
            for word in inp.lower().split():
                if word in words:
                    test_in[0][words.index(word)] = 1
            pred = nn.forward(model,test_in)[0]
            print(pred)
            pred_tag = np.argmax(pred)
            pred_resp = data["tags"][tags[pred_tag]]["responses"]
            pred_resp_text = pred_resp[int(np.random.random()*len(pred_resp))]
            if pred_tag == 2:
                ts = time.localtime()
                pred_resp_text = pred_resp_text % (wkday[ts.tm_wday], f"{ts.tm_hour}:{ts.tm_min}:{ts.tm_sec}")
            elif pred_tag == 3:
                pred_resp_text = pred_resp_text % (weather[random.randint(0,len(weather)-1)])
            print(pred_resp_text)
            tmp_ = gTTS(text=pred_resp_text,lang="en",slow=False)
            tmp_.save("tmp.mp3")
            os.system("mpg123 tmp.mp3")

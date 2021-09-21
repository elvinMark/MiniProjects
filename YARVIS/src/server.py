import requests
import json

from flask import Flask, request
import pafy
import vlc

from utils import *

app = Flask(__name__)

resources = {}

yarvis_browser = YarvisBrowser()
yarvis_system = YarvisSystem()

def check_words_and(list_words,q):
    for w in list_words:
        if not w in q:
            return False
    return True

def check_words_or(list_words,q):
    for w in list_words:
        if w in q:
            return True
    return False

@app.route("/execute_command",methods=["GET","POST"])
def execute_command():
    try:
        if request.method == "POST":
            data = json.loads(request.get_data())
            print(data)
            if "query" in data:
                q = data["query"].lower()
                if check_words_and(["play","youtube"],q):
                    song = q.replace("play","").replace("on","").replace("youtube","")
                    yarvis_browser.play_song_youtube(song)
                elif check_words_or(["stop","pause","resume"],q) and check_words_or(["music","video"], q):
                    yarvis_browser.pause_resume_song_youtube()
                elif check_words_and(["what","time"],q):
                    return yarvis_system.get_time()
                elif check_words_and(["what","date"],q):
                    return yarvis_system.get_date()
                elif check_words_and(["what","weather"],q):
                    return yarvis_browser.get_weather()
                elif check_words_and(["what"],q) and check_words_or(["is","are"],q) :
                    tmp_ = q.replace("what","").replace("is","").replace("are","")
                    return yarvis_browser.get_definition(tmp_)
                elif check_words_and(["search"],q):
                    tmp_ = q.replace("search","").replace("for","")
                    yarvis_browser.search_on_google(tmp_)
                elif check_words_and(["skip","ads"],q):
                    yarvis_browser.skip_ad_youtube()
                elif check_words_and(["open","emacs"],q):
                    yarvis_system.open_emacs()
                elif check_words_and(["open","facebook"],q):
                    yarvis_system.open_facebook()
                elif check_words_and(["open","mail"],q):
                    yarvis_system.open_mail()
                elif check_words_and(["open","youtube"],q):
                    yarvis_system.open_youtube()
                elif check_words_and(["open","notes"],q):
                    yarvis_system.open_gedit()
                elif check_words_and(["open","folder"],q):
                    yarvis_system.open_folder()
            return "Done sir"
        else:
            print("Unknow method")
            return "---Error---"
    except:
        print("request failed")

if __name__ == "__main__":
    app.run()

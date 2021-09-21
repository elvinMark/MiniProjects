from flask import Flask, request
import requests
import pafy
import vlc
import json

app = Flask(__name__)

resources = {}

def pause_song_youtube():
    if "media" in resources:
        resources["media"].pause()

def stop_song_youtube():
    if "media" in resources:
        resources["media"].stop()
    
def play_song_youtube(name_of_song):
    global resources
    if "media" in resources:
        resources["media"].stop()
    
    url = "https://content-youtube.googleapis.com/youtube/v3/search"

    querystring = {"part":"snippet","q":f"{name_of_song}","key":"AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"}

    payload = ""
    headers = {"X-Origin": "https://explorer.apis.google.com"}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    videoId = eval(response.text)["items"][0]["id"]["videoId"]
    url = f"https://www.youtube.com/watch?v={videoId}"
    video = pafy.new(url).getbest()
    media = vlc.MediaPlayer(video.url)
    resources["media"] = media
    media.play()

@app.route("/execute_command",methods=["GET","POST"])
def execute_command():
    try:
        if request.method == "POST":
            data = json.loads(request.get_data())
            print(data)
            if "query" in data:
                q = data["query"].lower()
                if "play" in q and "youtube" in q:
                    song = q.replace("play","").replace("on","").replace("youtube","")
                    play_song_youtube(song)
                elif "stop" in q and ("music" in q or "video" in q):
                    stop_song_youtube()
                elif "pause" in q and ("music" in q or "video" in q):
                    pause_song_youtube()
            return "success"
        else:
            print("Unknow method")
    except:
        print("request failed")

if __name__ == "__main__":
    app.run()

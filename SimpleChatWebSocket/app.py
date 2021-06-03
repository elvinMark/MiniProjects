from flask import Flask,render_template,request,render_template_string
from tinydb import TinyDB,Query
import time
import json
from gevent.pywsgi  import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
db = TinyDB("chat_db.json")

users = db.table("users")

query = Query()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.search(query.username == username)
        if user:
            user = user[0]
            if password == user["password"]:
                return render_template("chat.html",contacts=users.all(),user_id = user["id"],username=username)
            else:
                return render_template("login.html",message="Wrong passwod or wrong name")
        else:
            return render_template("login.html",message="Wrong passwod or wrong name")
    elif request.method == "GET":
        return render_template("login.html")

@app.route("/signup",methods=["GET"])
def signup():  
    return render_template("signup.html")

@app.route("/register",methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form["username"];
        password = request.form["password"];
        response = {"result":"User already existed"}
        user_id = str(len(users) + 1)
        if users.count(query.username == username) == 0:
            users.insert({"id":user_id,"username":username,"password":password})
            response["result"] = "User created succesfully!"
        return response

def get_opposite_id(chatid):
    ids = chatid.split("&")
    return ids[1] + "&" + ids[0]

@app.route("/pipe")
def pipe():
    if request.environ.get("wsgi.websocket"):
        ws = request.environ["wsgi.websocket"]
        while True:
            time.sleep(1)
            data = ws.receive()
            if data:
                data = json.loads(data)
                if data["op_type"] == "send":
                    chat_id = data["chat_id"]
                    content = data["content"]
                    
                    chat = db.table(chat_id)
                    cursor = len(chat)+1
                    
                    chat.insert({"cursor":cursor,"type":"send","content":content})
                    
                    chat = db.table(get_opposite_id(chat_id))
                    cursor = len(chat)+1
                
                    chat.insert({"cursor":cursor,"type":"receive","content":content})
                elif data["op_type"] == "receive":
                    chat_id = data["chat_id"]
                    cursor = int(data["cursor"])
                    
                    chat = db.table(chat_id)
                    messages = chat.search(query.cursor > cursor)
                    cursor += len(messages)

                    messages_container = render_template_string(
                    '{% for message in messages %}<div class="message-box"><div class="message-box-{{message.type}}"><p>{{message.content}}</p></div></div>{% endfor %}',messages=messages);
                    response = {"messages":messages_container,"cursor":cursor}
                    ws.send(json.dumps(response))
            else:
                break
    ws.close()
    return "Closing"

if __name__ == "__main__":
    server = WSGIServer(
        ("localhost",8080),
        app,
        handler_class = WebSocketHandler
    )
    server.serve_forever()

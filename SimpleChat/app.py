from flask import Flask,render_template,request,render_template_string
from tinydb import TinyDB,Query

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
        user = users.search(query.username == username)[0]
        if password == user["password"]:
            return render_template("chat.html",contacts=users.all(),user_id = user["id"],username=username)
        else:
            return render_template("login.html",message="Wrong passwod or wrong name")
    elif request.method == "GET":
        return render_template("login.html")

@app.route("/chat",methods=["POST"])
def chat():
    if request.method == "POST":
        chat_id = request.form["chat_id"]
        cursor = int(request.form["cursor"])
        chat = db.table(chat_id)
        messages = chat.search(query.cursor > cursor)
        cursor += len(messages)
        messages_container = render_template_string(
            '{% for message in messages %}<div class="message-box"><p>{{message.content}}</p></div>{% endfor %}',messages=messages);
        reponse = {"messages":messages_container,"cursor":cursor}
        return reponse
@app.route("/send",methods=["POST"])
def send():
    if request.method == "POST":
        chat_id = request.form["chat_id"]
        content = request.form["content"]

        chat = db.table(chat_id)
        cursor = len(chat)+1

        chat.insert({"cursor":cursor,"type":"send","content":content})

        chat = db.table(get_opposite_id(chat_id))
        cursor = len(chat)+1

        chat.insert({"cursor":cursor,"type":"receive","content":content})
        return 1

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
if __name__ == "__main__":
    app.run(host="localhost",port="8080")
    

from flask import Flask, render_template, render_template_string, request
from tinydb import TinyDB, Query
import time
import datetime

app = Flask(__name__)

db = TinyDB("twitter_db.json")
users = db.table("users")
query = Query()

tmp = 0
NUM_POST = 20

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password =  request.form["password"]
        db_user = users.search(query.username == user)
        if db_user:
            curr_user = db_user[0]
            if password == curr_user["username"]:
                user_data = {"idx":curr_user["idx"],"username":curr_user["username"],"num_followers":len(curr_user["followers"]),"num_following":len(curr_user["following"])}
                return render_template("mini_twitter.html",user_data=user_data)
            else:
                return render_template("index.html",message="Wrong password or username")
        return render_template("index.html",message="Wrong password or username")
    elif request.method == "GET":
        return render_template("index.html")

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        db_user = users.search(query.username == user)
        if db_user:
            return render_template("signup.html",message="User already registered")
        else:
            idx = len(users)
            users.insert({"idx":idx,"username":user,"password":password,"followers":[],"following":[]})
            return render_template("signup.html",message="User created Succesfully!")
    elif request.method == "GET":
        return render_template("signup.html")

@app.route("/post",methods=["POST"])
def post():
    if request.method == "POST":
        idx = int(request.form["idx"])
        user = users.search(query.idx == idx)[0]
        table = db.table("tweets_"+str(idx))
        ts = get_timestamp()
        table.insert({"idx":len(table),"timestamp":ts,"date":str(datetime.datetime.fromtimestamp(ts)),"user":user["username"],"message":request.form["message"],"comments":[],"likes":[]})
        return ""

@app.route("/tweets",methods=["POST"])
def tweets():
    if request.method == "POST":
        idx = int(request.form["idx"])
        ts = int(request.form["timestamp"])
        user = users.search(query.idx == idx)[0]
        following = user["following"]
        posts = get_last_tweets(idx,timestamp = ts)
        for i in following:
            posts += get_last_tweets(i,timestamp = ts)
        posts = sorted(posts,key = lambda k : k["timestamp"],reverse=True)
        response = {"last_timestamp":get_timestamp(),"data":render_template("posts.html",posts=posts[-NUM_POST:])}
        return response

@app.route("/search",methods=["POST"])
def search():
    if request.method == "POST":
        idx = int(request.form['idx'])
        user = users.search(query.idx == idx)[0]
        exclude_list = user["following"] + [idx]
        test_func = lambda s : s not in exclude_list
        users_list = users.search(query.idx.test(test_func))
    return render_template("search.html",contacts=users_list,user_id=idx)

@app.route("/follow",methods=["POST"])
def follow():
    if request.method == "POST":
        user_idx = int(request.form["user_id"])
        follow_idx = int(request.form["follow_id"])
        user = users.search(query.idx == user_idx)[0]
        follow = users.search(query.idx == follow_idx)[0]
        users.update({"following":user["following"] + [follow_idx]},query.idx == user_idx)
        users.update({"followers":user["followers"] + [user_idx]},query.idx == follow_idx)
        return ""
    return ""

@app.route("/comment",methods=["POST"])
def comment():
    if request.method == "POST":
        username = request.form["user"]
        post_idx = int(request.form["post_idx"])
        sender_idx = int(request.form["sender_idx"])
        print("hello")
        user_idx = int(users.search(query.username == username)[0]["idx"])
        sender = users.search(query.idx == sender_idx)[0]["username"]
        tweets = db.table("tweets_" + str(user_idx))
        prev_comments = tweets.search(query.idx==post_idx)[0]["comments"]
        curr_comment = {"message":request.form["comment"],"sender":sender,"date":str(datetime.datetime.fromtimestamp(get_timestamp()))}
        tweets.update({"comments" : prev_comments + [curr_comment]},query.idx == post_idx)
        return ""
def get_timestamp():
    return int(time.time())

def get_last_tweets(idx,last=5,timestamp=0):
    table = db.table("tweets_" + str(idx))
    arr = table.search(query.timestamp > timestamp)
    return arr[-last:]

if __name__ == "__main__":
    app.run(host="localhost",port=8080)

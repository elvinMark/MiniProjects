from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
    print(render_template("posts.html",test=range(10)))
    return render_template("index.html")


if __name__=="__main__":
    app.run()

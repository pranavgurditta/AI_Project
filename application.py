from flask import Flask,render_template,request
from flask import Flask, render_template, request
from werkzeug import secure_filename
import running_youtube
app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search_topic")
def search_topic():
    return render_template("search_topic.html")

@app.route("/result",methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      s=""
      for key, value in result.items():
          s=value
      ss=running_youtube.computeSimilarity("What is operating system?","An operating system is an interface between user ard hand Wave. It provides various functionally as process management, file management, memory management , It works like a government in real life .",s)
      return render_template("result.html",result = ss,url=img_url)
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask,render_template,request
from flask import Flask, render_template, request
from werkzeug import secure_filename
import running_youtube
app = Flask(__name__)




@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
		
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
      ss=running_youtube.main(s)
      print("ss is",ss)
      print("ss is",type(ss))
      img_url=[]
      url1=[]
      for video in ss:
            urls = "https://img.youtube.com/vi/"+video[0]+"/maxresdefault.jpg"
            img_url.append(urls)
            url_video="https://www.youtube.com/watch?v="+video[0]
            url1.append(url_video)
      return render_template("result.html",result = url1,url=img_url)
if __name__ == "__main__":
    app.run(debug=True)

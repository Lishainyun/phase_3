from flask import *
from util.s3_helper import upload_file_to_s3
from model.message import MessageModel
from flask_cors import CORS

app=Flask(__name__, static_folder="static", static_url_path="/")
CORS(app)

# API
@app.route("/upload",methods=["GET","POST"])
def upload_message():

    if request.method == "POST":
        imgFile = request.files['imgFile']
        text = request.form.get('text')
        upload_file_to_s3(imgFile)
        
        filename = imgFile.filename
        result = MessageModel.add_message(text,filename)
        return result
    else:
        result = MessageModel.get_message()
        return result

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
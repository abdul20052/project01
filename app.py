from flask import Flask, render_template, jsonify, request
import pymongo
from datetime import datetime
app = Flask(__name__)

client = pymongo.MongoClient("SECRET")
db = client["dblearningx"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    file = request.files['file_give']
    file2 = request.files['file2_give']
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    date = request.form["date_give"]

    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    extension2 = file2.filename.split('.')[-1]
    today2 = datetime.now()
    mytime2 = today2.strftime('%Y-%m-%d-%H-%M-%S')
    filename2 = f'file-{mytime2}.{extension2}'
    save_to2 = f'static/{filename2}'
    file2.save(save_to2)

    doc = {
        'file': filename,
        'profile_pic': filename2,
        'title': title_receive,
        'content': content_receive,
        'date': date
    }

    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
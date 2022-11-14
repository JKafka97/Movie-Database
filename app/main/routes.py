from flask import Blueprint, render_template, redirect, url_for, request
from apscheduler.schedulers.background import BackgroundScheduler
import urllib.request, json 

from app.extensions import mongo

def find_and_update_data():
    movies_connection = mongo.db.movies
    with urllib.request.urlopen("https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json") as url:
        datas = json.load(url)
        for data in datas:
            try:
                movies_connection.find_one_or_404({"name":data["name"]})
            except:
                movies_connection.insert_one(data)
                
scheduler = BackgroundScheduler()
scheduler.add_job(func=find_and_update_data, trigger="interval", seconds=300)
scheduler.start()

main = Blueprint('main', __name__)

@main.route('/')
def index():
    find_and_update_data()
    movies_connection = mongo.db.movies
    movies = movies_connection.find()
    return render_template('index.html', title='Movies', movies=movies)

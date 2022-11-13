from flask import Blueprint, render_template, redirect, url_for, request

from app.extensions import mongo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/add_movie', methods=['POST'])
def add_movie():
    movie_item = request.form.get('add-movie')
    movies_connection = mongo.db.movies
    movies_connection.insert_one({"text" : movie_item})
    return redirect(url_for('main.index'))
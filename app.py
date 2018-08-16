from setup_flask import app
from flask import Flask, flash, render_template, request, redirect, g
from flask_table import Table, Col
import sqlite3 as sql
import pickle
import pandas as pd 
import numpy as np 
import Recommenders

# DATABASE = './mymusic.db'
DATABASE = './mymusicsample_v3.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

@app.route('/')
def index():    
    return render_template('index.html')

@app.route("/songs", methods=['GET','POST'])
# def songs():
#     with app.app_context():      # for auto closing when out of scope
#         db = get_db()
#         cursor = db.execute("SELECT title, genre, duration, url_link FROM music LIMIT 50") # table is called musics
#         items = cursor.fetchall()
#         return render_template('songs.html', items=items)
def songs():
    return render_template('songs.html', data=data.to_dict())

@app.route('/history')
def history():    
    return render_template('history.html')

@app.route('/recommend')
def recommend():    
    return render_template('recommend.html', pm=pop_rec)

@app.route('/about')
def about():    
    return render_template('about.html')

""" For closing database """
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# run the application
if __name__ == "__main__":  
    # Load database
    data = load_data('mymusicsample_v3.pkl')

    # Create an instance of popularity based recommender class
    pm = Recommenders.popularity_recommender_py()
    pm.create(data, 'user_id', 'title')
    pop_rec = pm.recommend(data.iloc[0]['user_id'])     # recommend only once

    app.run(debug=True)


"""
Useful links:
https://ains.co/blog/things-which-arent-magic-flask-part-2.html

SQLITE3 COMMANDS
Open sqlite3 in terminal: sqlite3
Open file: .open FILENAME
List the tables in your database: .tables
List how the table looks: .schema tablename
Print the entire table: SELECT * FROM tablename;
List all of the available SQLite prompt commands: .help
"""

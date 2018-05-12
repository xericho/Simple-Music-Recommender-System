from setup_flask import app
from flask import Flask, flash, render_template, request, redirect, g
from display_tables import Results
from flask_table import Table, Col
import sqlite3 as sql

DATABASE = './mymusic.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

@app.route('/')
def index():    
    return render_template('index.html')

@app.route("/songs", methods=['GET','POST'])
def songs():
    with app.app_context():      # for auto closing when out of scope
        db = get_db()
        cursor = db.execute("SELECT title, genre, duration FROM musics LIMIT 50")
        items = cursor.fetchall()
        return render_template('songs.html', items=items)


@app.route('/history')
def history():    
    return render_template('history.html')

@app.route('/recommend')
def recommend():    
    return render_template('recommend.html')

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
    app.run(debug=True)


"""
Useful links:
https://ains.co/blog/things-which-arent-magic-flask-part-2.html
"""

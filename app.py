from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_table import Table, Col
import pickle
import pandas as pd 
import Recommenders as R

app = Flask(__name__)
app.secret_key = 'secret'   # needed to flash notifications

def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/dashboard/', methods=['GET','POST'])
def dashboard():
    user_id = None
    if request.method == "POST":
        user_id = request.form['user_id']
    return render_template('dashboard.html', 
                           df_clean=data_clean, 
                           pop_model=pop_rec, 
                           df=data, 
                           user_id=user_id, 
                           is_model=is_model)

# run the application
if __name__ == "__main__":  
    # Load database
    data = load_data('mymusicsample_v3.pkl')
    data_clean = data.drop_duplicates(subset='title')

    # Create an instance of popularity based recommender class
    pop_model = R.popularity_recommender_py()
    pop_model.create(data, 'user_id', 'title')
    pop_rec = pop_model.recommend(data.iloc[0]['user_id'])     # recommend only once

    # Initialize class for item similarity model
    is_model = R.item_similarity_recommender_py() 
    is_model.create(data, 'user_id', 'title')
    
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

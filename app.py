from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_table import Table, Col
import pickle
import pandas as pd 
import Recommenders as R
import ast

app = Flask(__name__)
app.secret_key = 'placeholder'   # needed to flash notifications


def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

@app.route('/', methods=['GET','POST'])
def index():
    hist = []
    return render_template('index.html', login_text='Login', url_link=default_url, hist=hist)

@app.route('/dashboard/', methods=['GET','POST'])
def dashboard():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        # Convert string dict to actual dict
        song_choice = ast.literal_eval(str(request.form.get('song_choice')))  
        if song_choice:
            user_id = song_choice['user_id']
            url_link = song_choice['url_link']
            title = data['df'].loc[data['df']['url_link'] == url_link, 'title'].iloc[0]
            data['history'].append([title, url_link])
        else:   # has to be a different user_id or started from '/'
            data['history'] = []    # reset history
            url_link = default_url  # reset url

    login_text = 'Logout' if user_id else 'Login'

    # return 'user_id'
    return render_template('dashboard.html', 
                           df=data['df'], 
                           pop_model=pop_rec, 
                           user_id=user_id, 
                           is_model=is_model,
                           hist=data['history'],
                           login_text=login_text,
                           url_link=url_link)

# run the application
if __name__ == "__main__":  
    # Load database
    df = load_data('mymusicsample_v3.pkl')

    # Create an instance of popularity based recommender class
    pop_model = R.popularity_recommender_py()
    pop_model.create(df, 'user_id', 'title')
    pop_rec = pop_model.recommend(df.iloc[0]['user_id'])     # recommend only once

    # Initialize class for item similarity model
    is_model = R.item_similarity_recommender_py() 
    is_model.create(df, 'user_id', 'title')

    # Initialize history of user choices
    data = {'df':df, 'history':[]}
    user_id = None
    default_url = 'https://w.soundcloud.com/player/?url=https%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F441889332&show_artwork=true&client_id=93e33e327fd8a9b77becd179652272e2%27'

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

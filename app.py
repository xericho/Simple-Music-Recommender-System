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
    return render_template('index.html', login_text='Login', url_link=default_url)

@app.route('/dashboard/', methods=['GET','POST'])
def dashboard():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        # Convert string dict to actual dict
        song_choice = ast.literal_eval(str(request.form.get('song_choice')))  
        if song_choice:
            user_id = int(song_choice['user_id'])
            url_link = song_choice['url_link']
            title = data['df'].loc[data['df']['url_link'] == url_link, 'title'].iloc[0]
            row = data['df'].loc[data['df']['url_link'] == url_link].iloc[0]
            row['user_id'] = user_id
            data['history'].append(row)
            df_combined = data['df'].append(pd.DataFrame(data['history']), ignore_index=True)
            models['item'].create(df_combined, 'user_id', 'title') 

        else:   # has to be a different user_id or started from '/'
            data['history'] = []    # reset history
            url_link = default_url  # reset url

    return render_template('dashboard.html', 
                           df=data['df'], 
                           pop_model=models['pop'], 
                           user_id=user_id, 
                           is_model=models['item'],
                           history=data['history'],
                           login_text='Logout',
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
    is_model = R.item_similarity_recommender_py(df, 'user_id', 'title') 

    # Store data and models in a dictionary
    data = {'df':df, 'history':[]}
    models = {'pop': pop_rec, 'item': is_model}
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

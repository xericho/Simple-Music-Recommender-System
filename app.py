from setup_flask import app
from db_setup import init_db
from forms import MusicSearchForm
from flask import flash, render_template, request, redirect
from models import Album

init_db()

@app.route('/')
def index():    
    return render_template('index.html')

@app.route("/songs")
def songs():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('songs.html', form=search)

@app.route('/songs/results')
def search_results(search):
    results = []
    search_string = search.data['search']
 
    if search.data['search'] == '':
        qry = db_session.query(Album)
        results = qry.all()
 
    if not results:
        flash('No results found!')
        return redirect('/songs')
    else:
        # display results
        return render_template('results.html', results=results)

@app.route('/history')
def history():    
    return render_template('history.html')

@app.route('/about')
def about():    
    return render_template('about.html')
# run the application
if __name__ == "__main__":  
    app.run(debug=True)


"""
Useful links:
https://ains.co/blog/things-which-arent-magic-flask-part-2.html
"""

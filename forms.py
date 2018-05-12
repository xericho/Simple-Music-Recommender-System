from wtforms import Form, StringField, SelectField
 
class MusicSearchForm(Form):
    choices = [('title', 'Title'),
               ('genre', 'Genre'),
               ('duration', 'Duration')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')

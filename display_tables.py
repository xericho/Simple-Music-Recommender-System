from flask_table import Table, Col
 
class Results(Table):
    # id = Col('Id', show=False)
    title = Col('title')
    genre = Col('genre')
    duration = Col('duration')

"""
Useful SQLite commands:
.schema
SELECT col_name FROM musics LIMIT 10
"""

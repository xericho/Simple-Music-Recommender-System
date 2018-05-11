import pandas as pd
from sqlalchemy import create_engine
# import mysql.connector

df = pd.read_pickle('clean_data.pkl')

engine = create_engine('sqlite:///music.db', echo=True)
df.iloc[0:100].to_sql(name='music', con=engine, index=False)


""" 
Source: https://www.blog.pythonlibrary.org/2017/12/13/flask-101-how-to-add-a-search-form/

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///mymusic.db', echo=True)
Base = declarative_base()
 
 
class Artist(Base):
    __tablename__ = "artists"
 
    id = Column(Integer, primary_key=True)
    name = Column(String)
 
    def __repr__(self):
        return "{}".format(self.name)
 
 
class Album(Base):
    __tablename__ = "albums"
 
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)
    publisher = Column(String)
    media_type = Column(String)
 
    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", backref=backref("albums", order_by=id))
 
# create tables
Base.metadata.create_all(engine)
"""


import sqlite3
from flask import g
from configure import Config

def get_db():
    #Connect to the database and return the connection
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(Config.DATABASE, check_same_thread=False)
        g.sqlite_db.row_factory = sqlite3.Row
    return g.sqlite_db

def close_db(error):
    #Close the database connection at the end of the request
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

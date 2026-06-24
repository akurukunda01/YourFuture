import psycopg2
import psycopg2.extras
from flask import g
from configure import Config

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        g.cursor = g.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return g.db, g.cursor


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


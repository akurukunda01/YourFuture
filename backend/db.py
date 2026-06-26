import psycopg2
import psycopg2.extras
from flask import g
from configure import Config


def get_db():
    """Return (connection, RealDictCursor) bound to the current request."""
    if "db" not in g:
        if not Config.DATABASE_URL:
            raise RuntimeError("DATABASE_URL is not configured")
        g.db = psycopg2.connect(Config.DATABASE_URL)
        g.cursor = g.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return g.db, g.cursor


def close_db(e=None):
    cursor = g.pop("cursor", None)
    if cursor is not None:
        cursor.close()
    db = g.pop("db", None)
    if db is not None:
        db.close()

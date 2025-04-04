# app.py
from flask import Flask
from flask_session import Session
from blueprints.jobs import jobs_bp
from blueprints.employer import employer_bp
from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from blueprints.site import site_bp
from configure import Config
import sqlite3
from db import get_db, close_db
from werkzeug.security import check_password_hash, generate_password_hash
print("app")
app = Flask(__name__)
app.config.from_object(Config) 
print(f"Database path: {Config.DATABASE}")
# Load configuration from config.py

# Initialize session handling
print("initializing session")
Session(app)

app.teardown_appcontext(close_db)

# Register blueprints
print("registering blueprints")
app.register_blueprint(jobs_bp)
app.register_blueprint(employer_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(site_bp)

if __name__ == "__main__":
    app.run(debug=True)




# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_session import Session
from blueprints.jobs import jobs_bp
from blueprints.employer import employer_bp
from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from blueprints.site import site_bp
from flask_cors import CORS
from configure import Config
from db import get_db, close_db
from werkzeug.security import check_password_hash, generate_password_hash
print("app")
app = Flask(__name__)
app.config.from_object(Config) 

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})


# Load configuration from config.py

# Initialize session handling
print("initializing session")
Session(app)

@app.teardown_appcontext
def teardown_db(exception):
    close_db()


# Register blueprints
print("registering blueprints")
app.register_blueprint(jobs_bp)
app.register_blueprint(employer_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(site_bp)


if __name__ == "__main__":
    app.run(debug=True, port=8000)




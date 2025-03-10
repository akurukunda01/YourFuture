from flask import Blueprint, render_template, request, session, redirect, send_from_directory, current_app
from helpers import login_required
from db import get_db


site_bp = Blueprint('site', __name__)

@login_required
@site_bp.route("/")
def index():
    if session.get("user_id"):
        name = session.get("name") #gets the current user's name
        if not name:
            name = "" #if there is no current user session, name is blank
        role = session.get("role") #get the current user's role
        if role == "employer":
            return render_template("employerhome.html", name = name) #if they are logged in as an employer, they will access the employer view
        elif role == "admin":
            return render_template("ahome.html",name=name)#if they are logged in as an admin, they will access the admin view
        return render_template("home.html", name = name) #else they will be acessing the student view
    elif not (request.path == "/login" or request.path == "/register"):
        return render_template("landing.html")


@site_bp.route("/credits")
def credits():
    return render_template("credits.html")



@login_required
@site_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    #sends the file path when called in the html
    upload_path = current_app.config['UPLOAD_PATH']
    return send_from_directory(upload_path, filename, mimetype='application/pdf')
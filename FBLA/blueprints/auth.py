from flask import Blueprint, render_template, request, redirect, session, jsonify
from helpers import apology
import sqlite3
from configure import Config
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

#login function
@auth_bp.route("/login", methods=["POST"])
def login():
    conn, cursor = get_db()
    username = request.form['username']
    password = request.form['password']
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    conn.close()
    if check_password_hash(user["user_password"],password):
        session["user_id"] = user["user_id"]
        session["username"] = user["username"]
        session["type"] = user["user_type"]
        print(session)
        return jsonify(user["user_type"]), 200
    else:
        return jsonify({"error": "password or username is incorrect"}), 400
    
    

#register function
@auth_bp.route("/register",methods = ["POST"])
def register():
    conn, cursor = get_db()
    username = request.form['username']
    password = request.form['password']
    conf_pass = request.form['confirm_password']
    user_type = request.form['user_type']
    org = request.form['user_org']
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    users = cursor.fetchall()
    print(users)
    if users:
        return jsonify({"error": "username is taken"}), 400
    if password!=conf_pass:
        return jsonify({"error": "your password and confirm password does not match"}), 400
    
    cursor.execute('INSERT INTO users (username, user_password, user_type, user_org, user_status) VALUES (%s,%s,%s,%s,%s)', (username, generate_password_hash(password, method='pbkdf2:sha256'), user_type, org,1))
    conn.commit()
    conn.close()
    return jsonify({"success": "user has been registered"}), 200
    
        

#logout function
@auth_bp.route("/logout")
def logout():
    session.clear() 
    return redirect("/login") 
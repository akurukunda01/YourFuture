from flask import Blueprint, render_template, request, redirect, session
from helpers import apology
import sqlite3
from configure import Config
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

auth_bp = Blueprint('auth', __name__)

#login function
@auth_bp.route("/login", methods=["GET","POST"])
def login():

    conn = get_db()
    cursor = conn.cursor()


    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
            
        #checks if user exsists and is approved by the admin to join
        cursor.execute("SELECT * FROM students WHERE email = ? AND status = ?", (email,"approved"))
        user = cursor.fetchone()

        #if user does not exsist or their entered password is not correct return apology
        if  user is not None:
            
            if not check_password_hash(user["password"],password):
                return apology("Invalid password")
        else:
            return apology("No account to this email")
        
        #set session data to the current users' data once they're logged in
        session["user_id"] = user["id"]
        session['name'] = user["name"]
        session["role"] = user["Role"]
        session["email"] = user["email"]
        
        conn.close()
        return redirect("/")
    conn.close()
    return render_template("login.html")

#register function
@auth_bp.route("/register",methods = ["GET", "POST"])
def register():

    conn = get_db() #connection to database
    cursor = conn.cursor() #creates cursor object to interact with database
    if request.method == "POST":
        #if user is submitting the form, retrieve its contents
        name = request.form.get("name") 
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        role = request.form.get("role")

        if password!=confirmation:
            #user's password and confirmed password input in the form do not match up
            return apology("Enter the correct password")
        
        #check if there is an account already registered to that email
        cursor.execute("SELECT email FROM students WHERE email = ?",(email,))
        exsisting_user = cursor.fetchone() 
                
        if exsisting_user:
            conn.close() # close connection to database
            return apology("Email already in use")
        
        #hashes user password for security reasons
        hash_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        
        #If there is no error in their registration, insert data into users table
        cursor.execute("INSERT INTO students (name,email,password, Role) VALUES (?,?,?,?)", (name, email, hash_password,role))
        conn.commit() #commit changes to database
        conn.close()
        return redirect("/login") #redirects the user to the login route
    conn.close()
    return render_template("register.html")#if no form submission occured yet, return the register page

#logout function
@auth_bp.route("/logout")
def logout():
    session.clear() #clears the current session as user has logged out
    return redirect("/login") 
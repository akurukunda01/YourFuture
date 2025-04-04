from flask import Blueprint, render_template, request, session, redirect, send_from_directory, current_app
from helpers import login_required
from db import get_db


site_bp = Blueprint('site', __name__)

@login_required
@site_bp.route("/")
def index():
    if session.get("user_id"):
        name = session.get("name")#gets the current user's name
        
        #get posts to display on home screen
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts")
        post_get = cursor.fetchall()
        posts = []
        if len(post_get)>5:
            for get in post_get[:5]:
                cursor.execute("SELECT name FROM students WHERE id = ?", (get["added_by"],))
                adder = cursor.fetchone()
                for add in adder:
                    posts.insert(0,{"added_by":add, "content":get["content"],"id":get["id"]})
        else:
            for get in post_get:
                cursor.execute("SELECT name FROM students WHERE id = ?", (get["added_by"],))
                adder = cursor.fetchone()
                for add in adder:
                    posts.insert(0,{"added_by":add, "content":get["content"],"id":get["id"]})
                    
        if not name:
            name = "" #if there is no current user session, name is blank
        role = session.get("role") #get the current user's role
        if role == "employer":
            cursor.execute("SELECT * FROM jobs WHERE added_by = ? AND status = ?", (session["user_id"],"approved"))
            myJobs = cursor.fetchall()
            job_port = []
            if len(myJobs) > 5:
                for job in myJobs[:5]: 
                    job_port.insert(0,{"company": job["company"], "company_role": job["company_role"], "pay": job["pay"]}) 
            else:
                for job in myJobs: 
                    job_port.insert(0,{"company": job["company"], "company_role": job["company_role"], "pay": job["pay"]}) 
            conn.close()
            return render_template("employerhome.html", name = name, posts = posts, portfolio=job_port) #if they are logged in as an employer, they will access the employer view
        elif role == "admin":
            cursor.execute("SELECT * FROM students WHERE status IS NULL")
            pendingUsers = cursor.fetchall()
            portfolio = []
            if len(pendingUsers)>5:
                for user in pendingUsers[:5]:
                    
                    portfolio.append({"name":user["name"], "email":user["email"], "role":user["role"]})
            else:
                for user in pendingUsers:
                    portfolio.append({"name":user["name"],"email":user["email"], "role":user["role"]})
            
            
            
            cursor.execute("SELECT * FROM jobs WHERE status IS NULL")
            pendingJobs = cursor.fetchall()
            jobs = []
            if len(pendingJobs)>5:
                for job in pendingJobs[:5]:
                    jobs.append({"company":job["company"], "role":job["company_role"]})
            else:
                for job in pendingJobs:
                    jobs.append({"company":job["company"], "role":job["company_role"]})
                
                    
            
            conn.close()
            return render_template("ahome.html",name=name,posts = posts,portfolio=portfolio, jobs = jobs)#if they are logged in as an admin, they will access the admin view
        
            
        cursor.execute("SELECT * FROM jobs WHERE status = ?", ("approved",))
        jobs = cursor.fetchall()  
        portfolio = []
        if len(jobs) > 5:
            for job in jobs[:5]: 
                portfolio.insert(0,{"company": job["company"], "company_role": job["company_role"], "pay": job["pay"]}) 
        else:
            for job in jobs: 
                portfolio.insert(0,{"company": job["company"], "company_role": job["company_role"], "pay": job["pay"]}) 
            
        conn.close()
        return render_template("home.html", name = name, posts = posts,portfolio = portfolio) #else they will be acessing the student view
        
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


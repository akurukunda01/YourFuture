from flask import Blueprint, render_template, request, session, redirect
from helpers import login_required
import sqlite3
from configure import Config
from db import get_db

admin_bp = Blueprint('admin', __name__)

#reviews jop postings
@login_required
@admin_bp.route("/reviewJobs", methods = ["GET","POST"])
def reviewJobs():

    conn = get_db()
    cursor = conn.cursor()

    #select all jobs 
    cursor.execute("SELECT * FROM jobs WHERE status IS NULL")
    jobs = cursor.fetchall()
    portfolio=[]

    for job in jobs:
        cursor.execute("SELECT name FROM students WHERE id = ?",(job["added_by"],))
        add = cursor.fetchone()
        portfolio.append({"company":job["company"], "id":job["id"],"company_role":job["company_role"],"pay":job["pay"], "Description": job["Description"],"adder":add[0] })
    

    if request.method == "POST":
        decision = request.form.get("action")

        if decision:
            action, job_id = decision.split('_')
            job_id = int(job_id)
            #if the job is approved set the status to approved in the table
            if action == "approve":
                cursor.execute("UPDATE jobs SET status = ? WHERE id = ?", ("approved", job_id))
            else:
                #if it's not approved, delete it from the table
                cursor.execute("DELETE FROM jobs WHERE id=?",(job_id,))
            conn.commit()
        conn.close()    
        return redirect("/reviewJobs")
    

    conn.close()
    return render_template("areview_jobs.html", portfolio = portfolio)

#review pending users
@login_required
@admin_bp.route("/reviewprofiles", methods = ["GET", "POST"])
def reviewProfiles():
    conn = get_db()
    cursor = conn.cursor()

    #select all user registers which have not been reviewed yet
    cursor.execute("SELECT * FROM students WHERE status IS NULL")
    user_applicants = cursor.fetchall()
    portfolio = []
    for user in user_applicants:
        #show all the non reviewed applicants to the admin
        portfolio.append({"id":user["id"],"name": user["name"], "email": user["email"], "role": user["Role"]})
    if request.method == "POST":
        decision = request.form.get("action")
        if decision:
            action, user_id = decision.split("_")
            user_id = int(user_id)
        
            if action == "approve":
                #if the user is approved, set their status to that
                cursor.execute("UPDATE students SET status = ? WHERE id = ?", ("approved", user_id))
                conn.commit()  # Ensure the changes are committed
            elif action == "decline":
                #if they are declined, delete them from the table
                cursor.execute("DELETE FROM students WHERE id = ?",(user_id,))
                conn.commit()
        conn.close()
        return redirect("/reviewprofiles")
    conn.close()
    return render_template("aprofiles.html", portfolio = portfolio)

#reviews student applications
@login_required
@admin_bp.route("/reviewapplicants", methods = ["GET", "POST"])
def application():
    conn = get_db()
    cursor = conn.cursor()

    #select all student applications
    cursor.execute("SELECT * FROM intrested_jobs")
    jobs = cursor.fetchall()
    portfolio=[]
    if jobs:
        
        for job in jobs:
            portfolio.append({"company":job["company"], "role": job["role"],"id": job["id"], "reason": job["reason"], "resume":job["resume"], "filepath": job["filepath"], "name": job["name"], "email": job["email"]})
    
    if request.method == "POST":
        #if the admin presses the remove button, delete the application
        decision = request.form.get("action")
        action, id = decision.split("_")
        id = int(id)
        cursor.execute("DELETE FROM intrested_jobs WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect("/reviewapplicants")
    conn.close()
    return render_template("aapplications.html", portfolio = portfolio)

@login_required
@admin_bp.route("/post",methods = ["GET","POST"])
def post():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    post_get = cursor.fetchall()
    posts = []
    for get in post_get:
        cursor.execute("SELECT name FROM students WHERE id = ?", (get["added_by"],))
        adder = cursor.fetchone()
        for add in adder:
            posts.insert(0,{"added_by":add, "content":get["content"],"id":get["id"]})
         
    if request.method == "POST":
        added_by = session['user_id']
        content = request.form.get('content')
        cursor.execute("INSERT INTO posts (added_by,content) VALUES (?,?) ", (added_by,content))
        conn.commit()
        conn.close()
        return redirect("/post")
    conn.close()
    return render_template("posts.html",posts = posts)

    
    

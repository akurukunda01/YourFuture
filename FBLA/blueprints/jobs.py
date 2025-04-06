from flask import Blueprint, render_template, request, session, redirect, current_app
from helpers import login_required, apology
import sqlite3,os
from configure import Config
from db import get_db
from werkzeug.utils import secure_filename

jobs_bp = Blueprint('jobs', __name__)

# student functions

@login_required #decorater which requires user to be logged in to view
@jobs_bp.route('/viewjobs', methods = ["GET", "POST"])
def view_jobs():
    conn = get_db()
    cursor1 = conn.cursor()#cursor 1 interacts with the jobs table
    cursor2 = conn.cursor()#cursor 2 interacts with the intrested_jobs table

    #select all jobs the user has applied to and store it in array
    interested_jobs_cursor = cursor2.execute("SELECT * FROM intrested_jobs WHERE user_id = ?", (session["user_id"], ))
    interested_jobs = []
    for interested_job in interested_jobs_cursor:
        interested_jobs.append(interested_job["job_id"])

    #select all the jobs postings that have been approved by the admin
    jobs = cursor1.execute("SELECT * FROM jobs WHERE status = ?",("approved",))

    portfolio = []
    for job in jobs:
        id = job["id"]
        #if a user has not already applied to a job show it to them
        check  = id in interested_jobs 
        if not check:
            portfolio.append({"company":job["company"], "id":job["id"],"company_role":job["company_role"],"pay":job["pay"], "Description": job["Description"]})

    if request.method == "POST":
        #Get data from user's application
        company = request.form.get("company")
        role = request.form.get("company_role")
        #find the table id of the job
        cursor1.execute("SELECT id FROM jobs WHERE company = ? AND company_role = ?",(company,role))
        job_id = cursor1.fetchone()
        job_id = job_id[0]
        
        reason = request.form.get("reason")
        #retrieve necessary user info from the session record
        email = session["email"]
        name = session["name"]
        

        #retrieves user's uploaded files
        file = request.files.get('resume')

       
    
        if file.filename == '': #checks if there is a filename
            file_ext = filename.rsplit('.', 1)[1].lower()
            if file_ext not in current_app.config["UPLOAD_EXTENSIONS"]:
                conn.close()#checks if the user uploaded an allowed file type
                return apology("no selected files")
            
        filename = secure_filename(f"{session['user_id']}_{job_id}_{file.filename}") #creates a secured filename to avoid hacker interference
        
        file_path = (os.path.join(current_app.config["UPLOAD_PATH"], filename)) #retrieves the file path of the uploaded file from the folder

        if os.path.exists(file_path): #checks is the file has already been added
            conn.close()
            return apology('File already exists. Please rename your file.')
        
        
        
        
        file.save(file_path) #saves file path



        #inserts necessary application data into intrested_jobs table
        cursor2.execute("INSERT INTO intrested_jobs (job_id,user_id,name,email,company, role, reason,resume,filepath) VALUES (?,?,?,?,?,?,?,?,?)",(job_id,session["user_id"],name,email,company,role,reason,filename,file_path))
        conn.commit()
        conn.close()
        return redirect("/viewjobs")


    conn.close()
    return render_template('userview_jobs.html', portfolio=portfolio)

@login_required
@jobs_bp.route('/search', methods = ['GET'])
def Search():  
    item = request.args.get('query')
    if item:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM JOBS WHERE (company LIKE ? OR company_role LIKE ?) AND status = ?",('%'+item+'%','%'+item+'%', "approved"))
        jobs = cursor.fetchall()
        if jobs:
            conn.close()
            return render_template("userview_jobs.html",portfolio = jobs)
    conn.close()
    return redirect('/viewjobs')
       
# Main Profile Route (for name, email, bio)
@jobs_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    conn = get_db()
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor.execute("SELECT * FROM profile WHERE id = ?", (session["user_id"],))
    profile = cursor.fetchone()
    cursor1.execute("SELECT * FROM intrested_jobs WHERE user_id = ?",(session["user_id"],))
    jobs = cursor1.fetchall()
    portfolio=[]
    if jobs:
        for job in jobs:
            portfolio.append({"company":job["company"], "role": job["role"], "id": job["id"], "reason": job["reason"], "resume":job["resume"], "filepath": job["filepath"]})
    
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        bio = request.form.get('bio')
        cursor.execute("SELECT * FROM profile WHERE id = ?",(session["user_id"],))
        exsisting_Profile = cursor.fetchone()
        if exsisting_Profile:
            cursor.execute("UPDATE profile SET name = ?, email = ?, bio = ? WHERE id = ?", (name, email, bio, session["user_id"]))
        else:
            cursor.execute("INSERT INTO profile VALUES (?,?,?,?,?,?)",(name,email,session["user_id"],bio,None,None))
        conn.commit()
        conn.close()
        return redirect('/profile')

    conn.close()
    return render_template('profile.html', profile=profile,portfolio=portfolio)

# Separate Route for Adding Skill
@jobs_bp.route('/add-skill', methods=['POST'])
@login_required
def add_skill():
    skill = request.form.get('new_skill')
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT skills FROM profile WHERE id = ?", (session["user_id"],))
    skills = cursor.fetchone()
    if skills[0]!=None:
        skills = skills[0] + ',' + skill
    else:
        skills = skill
    
    cursor.execute("UPDATE profile SET skills = ? WHERE id = ?", (skills, session["user_id"]))
    conn.commit()
    conn.close()

    return redirect('/profile')

# Separate Route for Adding Info
@jobs_bp.route('/add-info', methods=['POST'])
@login_required
def add_info():
    additional_info = request.form.get('new_additional_info')
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT info FROM profile WHERE id = ?", (session["user_id"],))
    info = cursor.fetchone()[0]
    
    if info:
        info = info + ',' + additional_info
    else:
        info = additional_info
    cursor.execute("UPDATE profile SET info = ? WHERE id = ?", (info, session["user_id"]))
    conn.commit()
    conn.close()

    return redirect('/profile')


@login_required
@jobs_bp.route('/pinnedjobs', methods = ["GET", "POST"])
def pinnedJobs():
    conn = get_db()
    cursor = conn.cursor()
    
    #selects current user's applications
    cursor.execute("SELECT * FROM intrested_jobs WHERE user_id = ?",(session["user_id"],))
    jobs = cursor.fetchall()
    portfolio=[]
    if jobs:
        for job in jobs:
            portfolio.append({"company":job["company"], "role": job["role"], "id": job["id"], "reason": job["reason"], "resume":job["resume"], "filepath": job["filepath"]})
    if request.method == "POST":
        #if remove button is pressed remove application
        decision = request.form.get("action")
        action, id = decision.split("_") 
        id = int(id)
        #deletes from table where the id matches the application id that the user wanted to remove
        cursor.execute("DELETE FROM intrested_jobs WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect("/pinnedjobs")

    
    conn.close()
    return render_template("sapplications.html", portfolio = portfolio)

@login_required
@jobs_bp.route('/viewposts', methods = ["GET"])
def seePosts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    get_post = cursor.fetchall()
    posts = []
    for get in get_post:
        cursor.execute("SELECT name FROM students WHERE id = ?", (get["added_by"],))
        adder = cursor.fetchone()
        for add in adder:
            posts.insert(0,{"added_by":add, "content":get["content"],"id":get["id"]})
    conn.close()
    return render_template("sPosts.html", posts = posts)

@login_required
@jobs_bp.route("/searchHome")
def searchHome():
    item = request.args.get('query')
    if item:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profile WHERE name LIKE ?",('%'+item+'%',))
        profile = cursor.fetchone()
        if profile:  
            conn.close()
            return render_template("searchResults.html",profile=profile)
    return redirect('/')

    







    
        
    
    





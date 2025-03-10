from flask import Blueprint, render_template, request, session, redirect
from helpers import login_required, apology
import sqlite3
from configure import Config
from db import get_db

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
            if file_ext not in app.config["UPLOAD_EXTENSIONS"]:#checks if the user uploaded an allowed file type
                return apology("no selected files")
            
        filename = secure_filename(f"{session['user_id']}_{job_id}_{file.filename}") #creates a secured filename to avoid hacker interference
        
        file_path = (os.path.join(app.config["UPLOAD_PATH"], filename)) #retrieves the file path of the uploaded file from the folder

        if os.path.exists(file_path): #checks is the file has already been added
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
    







    
        
    
    





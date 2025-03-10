from flask import Blueprint, render_template, request, session, redirect
from helpers import login_required
import sqlite3
from configure import Config
from db import get_db

employer_bp = Blueprint('employer', __name__)

@login_required
@employer_bp.route("/myjobs", methods = ["GET", "POST"])
def myJobs():
    conn = get_db()
    cursor = conn.cursor()
    #selects all approved jobs the employer has posted
    cursor.execute("SELECT * FROM jobs WHERE added_by = ? AND status = ?", (session["user_id"],"approved"))
    jobs = cursor.fetchall()
    portfolio = []
    for job in jobs:
        portfolio.append({"company":job["company"], "id":job["id"],"company_role":job["company_role"],"pay":job["pay"], "Description": job["Description"]})

    if request.method == "POST":
        # if they press remove button delete the posting
        if "remove" in request.form:
            remove = request.form.get("remove")
            action,job_id = remove.split("_")
            job_id = int(job_id)
            #delete from both tables the one storing the user applications and the one storing the jobs
            cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
            cursor.execute("DELETE FROM intrested_jobs WHERE job_id = ?", (job_id,))
            conn.commit()
        if "add" in request.form:
            #if the user wants to add a postint, get necessary data
            company = request.form.get("company")
            company_role = request.form.get("company_role")
            pay = request.form.get("pay")
            desc = request.form.get("Description")
            #insert the posting into the table so it can be sent for admin review
            cursor.execute("INSERT INTO jobs (company,company_role,pay,added_by, Description) VALUES (?,?,?,?,?)", (company,company_role, pay, session["user_id"], desc))
            conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    return render_template("ejobs.html", portfolio = portfolio)


@login_required
@employer_bp.route("/applications")
def viewApplications():
    conn = get_db()
    cursor = conn.cursor()

    #select all the jobs which were added by the current user
    jobs = cursor.execute("SELECT * FROM jobs WHERE added_by = ?", (session["user_id"],))
    postedJobs = []
    for job in jobs:
        postedJobs.append(job["id"])
    
    #select all approved student job applications
    cursor.execute("SELECT * FROM intrested_jobs")
    jobs = cursor.fetchall()
    portfolio=[]
    #if there are student applications and there are applications to a job posted by the current employer send it to them for view
    if jobs:
        
        for job in jobs:
            check = job["job_id"] in postedJobs
            if check:
                portfolio.append({"company":job["company"], "role": job["role"], "id": job["id"], "reason": job["reason"], "resume":job["resume"], "filepath": job["filepath"],  "name": job["name"], "email": job["email"]})
    conn.close()
    return render_template("eapplications.html", portfolio = portfolio)
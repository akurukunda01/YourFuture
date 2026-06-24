from flask import Blueprint, render_template, request, session, redirect, current_app, jsonify
from helpers import login_required, apology
import os
from configure import Config
from db import get_db
from werkzeug.utils import secure_filename
from flask_cors import CORS

jobs_bp = Blueprint('jobs', __name__, url_prefix="/api")

# student functions

#@login_required #decorater which requires user to be logged in to view
@jobs_bp.route('/viewjobs', methods = ["GET"])
def view_jobs():
    print(session)
    conn, cursor = get_db()
    if request.method == "GET":
        cursor.execute("SELECT * FROM saved_opps")
        saved = cursor.fetchall()
        keys = []
        for save in saved:
            keys.append(save["opp_key"])
        cursor.execute(
            "SELECT * FROM jobs WHERE job_status = %s",(1,)
        )
        jobs = cursor.fetchall()
        portfolio = []
        if jobs:
            for job in jobs:
                if job["job_id"] not in keys:
                    portfolio.append({
                        "job_id": job["job_id"],
                        "company": job["company"],
                        "company_role": job["company_role"],
                        "pay": job["pay"],
                        "job_description": job["job_description"],
                        "job_location": job["job_location"],
                        "company_logo_url": job["company_logo_url"]
                    })
                else:
                    portfolio.append({
                        "job_id": job["job_id"],
                        "company": job["company"],
                        "company_role": job["company_role"],
                        "pay": job["pay"],
                        "job_description": job["job_description"],
                        "job_location": job["job_location"],
                        "company_logo_url": job["company_logo_url"],
                        "saved":1
                    })


        conn.close()
        return jsonify(portfolio)

@jobs_bp.route('/apply', methods=["POST"])
def apply():
    conn, cursor = get_db()
    name = request.form['name']
    email = request.form['email']
    q1 = request.form['q1']
    q2 = request.form['q2']
    q3 = request.form['q3']
    resume = request.files.get('resume')
    opp_id = request.form['opp_id']
    opp_type = request.form['opp_type']
    if opp_type == 'job':
        cursor.execute("SELECT company_role FROM jobs WHERE job_id=%s",(opp_id,))
        job = cursor.fetchone()
        cursor.execute("SELECT opp_id FROM opportunities WHERE opp_name = %s", (job["company_role"],))
        opp_id = cursor.fetchone()["opp_id"]
    elif opp_type == 'unpaid':
        cursor.execute("SELECT unpaid_role FROM unpaid WHERE unpaid_id=%s", (opp_id,))
        role = cursor.fetchone()["unpaid_role"]
        cursor.execute("SELECT opp_id FROM opportunities WHERE opp_name = %s", (role,))
        opp_id = cursor.fetchone()["opp_id"]
    if not(name or email or q1 or q2 or q3):
        return jsonify({"error": "There is something missing"}), 400
    if resume:
        filename = secure_filename(resume.filename)
        save_path = os.path.join('uploads', filename)
        resume.save(save_path)
        cursor.execute("INSERT INTO applications (opp_id, entered_name, entered_email, q1, q2, q3, resume_path, opp_type) VALUES(%s, %s, %s, %s,%s,%s,%s, %s)", (opp_id,name,email,q1,q2,q3, save_path, opp_type))
    else:
        return jsonify({"error": "No Resume uploaded"}), 400
    conn.commit()
    conn.close()
    return jsonify({"message": "Application submitted successfully"}), 200

@jobs_bp.route("/saveopp", methods=["POST"])
def save():
    print(session.get("user_id"))
    conn, cursor = get_db()
    data = request.get_json()
    opp_type = data["opp_type"]
    opp_key = data["opp_key"]
    if not(opp_type or opp_key):
        return jsonify({"error": "there is something missing"}), 400
    cursor.execute("INSERT INTO saved_opps (opp_type, opp_key, user_id) VALUES (%s, %s,%s)", (opp_type, opp_key, session["user_id"]))
    conn.commit()
    conn.close()
    return jsonify({"sucess": "job has been saved"}), 200

@jobs_bp.route('/viewunpaid', methods=['GET'])
def getUnpaid():
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM unpaid WHERE unpaid_status=%s", (1,))
    opps = cursor.fetchall()
    conn.close()
    portfolio = []
    if opps:
        for opp in opps:
            portfolio.append({
                "unpaid_id": opp["unpaid_id"],
                "organization": opp["organization"],
                "org_logo": opp["org_logo"],
                "unpaid_desc": opp["unpaid_desc"],
                "unpaid_location": opp["unpaid_location"],
                "unpaid_role": opp["unpaid_role"],
                "date_added": opp["date_added"]
            })
        return jsonify(portfolio)

@jobs_bp.route('/unpaid/<int:id>', methods=['GET'])
def unpaidDetails(id):
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM unpaid WHERE unpaid_id = %s", (id,))
    opp = cursor.fetchone()
    conn.close()
    if opp:
        dateAdded = opp["date_added"].strftime('%Y-%m-%d')
        return jsonify({
            "unpaid_id": opp["unpaid_id"],
            "organization": opp["organization"],
            "org_logo": opp["org_logo"],
            "unpaid_desc": opp["unpaid_desc"],
            "unpaid_location": opp["unpaid_location"],
            "unpaid_role": opp["unpaid_role"],
            "date_added": dateAdded
        })
    else:
        return jsonify({"error": "opportunity not found"}), 404

@jobs_bp.route('/viewevents', methods=['GET'])
def getEvents():
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM events WHERE event_status = %s", (1,))
    events = cursor.fetchall()
    conn.close()
    portfolio = []
    if events:
        for event in events:
            date = event["event_date"].strftime('%Y-%m-%d')
            portfolio.append({
                "event_id":event["event_id"],
                "organization":event["organization"],
                "org_logo": event["org_logo"],
                "date_added": event['date_added'],
                "event_date": date,
                "event_desc":event["event_desc"],
                "event_location": event["event_location"],
                "event_name": event["event_name"]
            })
    return jsonify(portfolio)

@jobs_bp.route('/events/<int:id>', methods=["GET"])
def eventDetails(id):
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (id,))
    event = cursor.fetchone()
    conn.close()
    if event:
        dateAdded = event["date_added"].strftime('%Y-%m-%d')
        dateEvent = event["event_date"].strftime('%Y-%m-%d')
        return jsonify({
            "event_id":event["event_id"],
            "organization":event["organization"],
            "org_logo": event["org_logo"],
            "date_added": dateAdded,
            "event_date": dateEvent,
            "event_desc":event["event_desc"],
            "event_location": event["event_location"],
            "event_name": event["event_name"]
        })
    else:
        return jsonify({"error":"Event not found"}), 404

@jobs_bp.route('/job/<int:id>', methods=['GET'])
def jobDetails(id):
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (id,))
    job = cursor.fetchone()
    conn.close()
    if job:
        return jsonify({
            "job_id": job["job_id"],
            "company_role": job["company_role"],
            "company": job["company"],
            "pay": job["pay"],
            "description" : job["job_description"],
            "location": job["job_location"],
            "company_logo_url":job["company_logo_url"]
        })
    else:
        return jsonify({"error":"Job not Found"}), 404
    
#@login_required
@jobs_bp.route('/search', methods = ['GET'])
def Search():  
    item = request.args.get('q')
    portfolio = []
    if item:
        conn, cursor = get_db()
        cursor.execute(
            "SELECT * FROM opportunities WHERE (opp_name ILIKE %s OR opp_org ILIKE %s) AND opp_status = %s",
            ('%' + item + '%', '%' + item + '%',1)
        )
        list = cursor.fetchall()
        if list:
            for l in list:
                key = l["opp_key"]
                if l["opp_type"] == 'job':
                    print(l, key)
                    cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (key,))
                    job = cursor.fetchone()
                    portfolio.append({
                        "job_id": job["job_id"],
                        "company": job["company"],
                        "company_role": job["company_role"],
                        "pay": job["pay"],
                        "description": job["job_description"],
                        "job_location": job["job_location"],
                        "company_logo_url":job["company_logo_url"],
                        "type": "job"
                    })
                elif (l["opp_type"]) == 'unpaid':
                    cursor.execute("SELECT * FROM unpaid WHERE unpaid_id= %s", (key,))
                    opp = cursor.fetchone()
                    portfolio.append({
                        "unpaid_id": opp["unpaid_id"],
                        "organization": opp["organization"],
                        "org_logo": opp["org_logo"],
                        "unpaid_desc": opp["unpaid_desc"],
                        "unpaid_location": opp["unpaid_location"],
                        "unpaid_role": opp["unpaid_role"],
                        "date_added": opp["date_added"],
                        "type": "unpaid"
                    })
                elif (l["opp_type"]) == 'event':
                    cursor.execute("SELECT * FROM events WHERE event_id = %s", (key,))
                    event = cursor.fetchone()
                    date = event["event_date"].strftime('%Y-%m-%d')
                    portfolio.append({
                    "event_id":event["event_id"],
                    "organization":event["organization"],
                    "org_logo": event["org_logo"],
                    "date_added": event['date_added'],
                    "event_date": date,
                    "event_desc":event["event_desc"],
                    "event_location": event["event_location"],
                    "event_name": event["event_name"],
                    "type": "event"
                })
            conn.close()
            return jsonify(portfolio)
    return jsonify([])

       
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

    







    
        
    
    





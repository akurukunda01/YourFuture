from flask import Blueprint, render_template, request, session, redirect, send_from_directory, current_app, jsonify
from helpers import login_required
from db import get_db
import os
from werkzeug.utils import secure_filename

site_bp = Blueprint('site', __name__, url_prefix='/api')


@site_bp.route('/getmessages', methods=['GET'])
def getMessages():
    conn, cursor = get_db()
    user_id = session["user_id"]

    # Get all messages involving the current user
    cursor.execute("""
        SELECT m.*, s.username AS sender_username, r.username AS receiver_username
        FROM messages m
        JOIN users s ON m.sender_id = s.user_id
        JOIN users r ON m.reciever_id = r.user_id
        WHERE m.sender_id = %s OR m.reciever_id = %s
        ORDER BY m.date ASC
    """, (user_id, user_id))

    messages = cursor.fetchall()
    conn.close()

    inbox = {}

    for m in messages:
        # Identify the conversation partner (the other person)
        if m["sender_id"] == user_id:
            other_id = m["reciever_id"]
            other_username = m["receiver_username"]
        else:
            other_id = m["sender_id"]
            other_username = m["sender_username"]

        # Group by the other person's username
        if other_username not in inbox:
            inbox[other_username] = []

        inbox[other_username].append({
            "id": m["msg_id"],
            "content": m["msg_content"],
            "date": m["date"],
            "sender_id": m["sender_id"],
            "sender_username": m["sender_username"],
            "reciever_id": m["reciever_id"],
            "reciever_username": m["receiver_username"]
        })

    return jsonify(inbox)


@site_bp.route("/sendmessages", methods=["POST"])
def sendMessages():
    conn, cursor = get_db()
    sender = session["username"]
    reciever = request.form['reciever']
    msg_content = request.form['msg_content']

    if not(sender and reciever and msg_content):
        return jsonify({"error": "there is something missing"}), 400
    
    cursor.execute("SELECT user_id FROM users WHERE username =%s", (sender,))
    sender_id = cursor.fetchone()["user_id"]
    cursor.execute("SELECT user_id FROM users WHERE username =%s", (reciever,))
    reciever_id = cursor.fetchone()["user_id"]

    cursor.execute("INSERT INTO messages (sender_id, reciever_id, msg_content) VALUES (%s, %s, %s)", (sender_id, reciever_id, msg_content))
    conn.commit()
    conn.close()
    return jsonify({"sucess": "message has been added"}), 200

@site_bp.route("/reciever")
def revieverSearch():
    item = request.args.get('q')
    portfolio = []
    if item:
        conn, cursor = get_db()
        cursor.execute(
            "SELECT * FROM users WHERE (username ILIKE %s) AND user_status = %s",
            ('%' + item + '%',1)
        )
        results = cursor.fetchall()
        if results:
            for res in results:
                portfolio.append(res["username"])
    conn.close()
    return jsonify(portfolio)

@site_bp.route("/getposts", methods=["GET"])
def getPosts():
    conn,cursor = get_db()
    cursor.execute("SELECT * FROM forum WHERE post_status=%s", (1,))
    posts = cursor.fetchall()
    portfolio = []
    if posts:
        for post in posts:
            cursor.execute("SELECT * FROM users WHERE user_id=%s", (post["added_by"],))
            obj = cursor.fetchone()
            adder = obj["username"]
            adder_name = obj["full_name"]
            adder_pic = obj["profile_pic"]
            user_org = obj["user_org"]
            portfolio.append({
                "post_id":post["post_id"],
                "post_content":post["post_content"],
                "added_by": adder,
                "post_media": post["post_media"],
                "post_time":post["post_time"],
                "full_name":adder_name,
                "profile_pic":adder_pic,
                "user_org":user_org
            })
    conn.close()
    return jsonify(portfolio)

@site_bp.route('/addpost', methods=["POST"])
def addPost():
    conn,cursor = get_db()
    post_content = request.form['post_content']
    post_media = request.files.get('post_media')
    if not (post_content):
        return jsonify({"error": "Something missing"}), 400
    if post_media:
        filename = secure_filename(post_media.filename)
        save_path = os.path.join('uploads', filename)
        post_media.save(save_path)
        cursor.execute("INSERT INTO forum (added_by, post_content, post_media, post_status) VALUES (%s,%s,%s,%s)", (session["user_id"],post_content, f'FBLA/uploads/{filename}', 1))
    cursor.execute("INSERT INTO forum (added_by, post_content, post_status) VALUES (%s,%s,%s)", (session["user_id"],post_content, 1))
    
    conn.commit()
    conn.close()
    return jsonify({"success": "post has been added"}), 200

@site_bp.route("/postsearch", methods=["GET"])
def postSearch():
    item = request.args.get('q')
    portfolio = []
    if item:
        conn, cursor = get_db()
        cursor.execute(
            """
            SELECT forum.*
            FROM forum
            JOIN users ON forum.added_by = users.user_id
            WHERE (users.username ILIKE %s OR forum.post_content ILIKE %s)
            AND forum.post_status = %s
            """,
            ('%' + item + '%', '%' + item + '%', 1)
        )


        results = cursor.fetchall()
        if results:
            for res in results:
                    cursor.execute("SELECT * FROM users WHERE user_id=%s", (res["added_by"],))
                    adder = cursor.fetchone()["username"]
                    portfolio.append({
                        "post_id":res["post_id"],
                        "post_content":res["post_content"],
                        "added_by": adder,
                        "post_media": res["post_media"],
                        "post_time":res["post_time"]
                    })
            
    conn.close()
    return jsonify(portfolio)

@site_bp.route("/myprofile")
def getProfile():
    conn,cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE user_id=%s AND user_status=%s",(session["user_id"],1))
    user = cursor.fetchone()
    cursor.execute("SELECT * FROM experiences WHERE user_id=%s", (session["user_id"],))
    experiences = cursor.fetchall()
    cursor.execute("SELECT * FROM saved_opps WHERE user_id=%s", (session["user_id"],))
    saved = cursor.fetchall()
    saved_opps = []
    for save in saved:
        opp = []
        if save["opp_type"] == 'job':
            cursor.execute("SELECT * FROM jobs WHERE job_id = %s and job_status = %s", (save["opp_key"], 1,))
            opp = cursor.fetchone()
            saved_opps.append({
                "opp_type":"job",
                "opp": opp
            })
        elif save["opp_type"] == 'unpaid':
            cursor.execute("SELECT * FROM unpaid WHERE unpaid_id = %s and unpaid_status = %s", (save["opp_key"], 1,))
            opp = cursor.fetchone()
            saved_opps.append({
                "opp_type":"unpaid",
                "opp": opp
            })
        elif save["opp_type"] == 'event':
            cursor.execute("SELECT * FROM events WHERE event_id = %s and event_status = %s", (save["opp_key"], 1,))
            opp = cursor.fetchone()
            saved_opps.append({
                "opp_type":"event",
                "opp": opp
            })
    print(f'This is the saved opp: {saved_opps}')
        
    cursor.execute("SELECT * FROM forum where added_by=%s and post_status=%s", (session["user_id"],1))
    posts = cursor.fetchall()
    portfolio = []
    if posts:
        for post in posts:
            cursor.execute("SELECT * FROM users WHERE user_id=%s", (post["added_by"],))
            adder = cursor.fetchone()["username"]
            portfolio.append({
                "post_id":post["post_id"],
                "post_content":post["post_content"],
                "added_by": adder,
                "post_media": post["post_media"],
                "post_time":post["post_time"]
            })
    conn.close()
    return jsonify({
        "user":user,
        "experiences":experiences,
        "posts":portfolio,
        "saved_opps":saved_opps
    })
@site_bp.route("/profile/<int:id>")
def retrieveProfile(id):
    conn,cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE user_id=%s AND user_status=%s",(id,1))
    user = cursor.fetchone()
    cursor.execute("SELECT * FROM experiences WHERE user_id=%s", (session["user_id"],))
    experiences = cursor.fetchall()
    conn.close()
    return jsonify({
        "user":user,
        "experiences":experiences
    })


    

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



#@login_required
@site_bp.route('/FBLA/uploads/<filename>')
def uploaded_file(filename):
    #sends the file path when called in the html
    upload_path = current_app.config['UPLOAD_PATH']
    return send_from_directory('uploads', filename)


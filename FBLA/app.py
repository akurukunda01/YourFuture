import sqlite3
import  os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask, flash, redirect, render_template, request, session,g, send_from_directory
from flask_session import Session
from helpers import login_required,apology

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False #Session will expire when browser is closed
app.config["SESSION_TYPE"] = "filesystem" #store session data on server's filesytem
app.config['TEMPLATES_AUTO_RELOAD'] = True #automatically reloads templates when modified
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #disables chaching for static files
app.config["MAX_CONTENT_LENGTH"] = 1024*1024 #max size of the file
app.config["UPLOAD_EXTENSIONS"] = [".pdf"] #possible file types for user to upload
app.config["UPLOAD_PATH"] = 'uploads/' #saves the file path





Session(app) #Inializes session handling for flask app

db = "./SQL/student.db" #SQLite3 dtatbase path

def get_db():
    if not hasattr(g, 'sqlite_db'): #checks if database connection is already established
        g.sqlite_db = sqlite3.connect(db, check_same_thread=False) #creates new database connection
        g.sqlite_db.row_factory = sqlite3.Row  # Allows column access by name, instead of index
    return g.sqlite_db #return database connection

@app.teardown_appcontext
def close_db(error):
    """Close the database connection at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()






@login_required
@app.route("/")
def index():
    name = session.get("name") #gets the current user's name
    if not name:
        name = "" #if there is no current user session, name is blank
    role = session.get("role") #get the current user's role
    if role == "employer":
        return render_template("employerhome.html", name = name) #if they are logged in as an employer, they will access the employer view
    elif role == "admin":
        return render_template("ahome.html",name=name)#if they are logged in as an admin, they will access the admin view
    return render_template("home.html", name = name) #else they will be acessing the student view

@app.route("/register",methods = ["GET", "POST"])
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
            flash("Enter the correct password")
        
        #check if there is an account already registered to that email
        cursor.execute("SELECT email FROM students WHERE email = ?",(email,))
        exsisting_user = cursor.fetchone() 
                
        if exsisting_user:
            conn.close() # close connection to database
            flash("Email already in use")
        
        #hashes user password for security reasons
        hash_password = generate_password_hash(password, method='pbkdf2:sha256')
        print(hash_password)
        
        #If there is no error in their registration, insert data into users table
        cursor.execute("INSERT INTO students (name,email,password, Role) VALUES (?,?,?,?)", (name, email, hash_password,role))
        conn.commit() #commit changes to database
        conn.close()
        return redirect("/login") #redirects the user to the login route
    conn.close()
    return render_template("register.html")#if no form submission occured yet, return the register page




@app.route("/login", methods=["GET","POST"])
def login():

    conn = get_db()
    cursor = conn.cursor()


    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
            
        #checks if user exsists and is approved by the admin to join
        cursor.execute("SELECT * FROM students WHERE email = ? AND status = ?", (email,"approved"))
        user = cursor.fetchone()
        print(user)

        #if user does not exsist or their entered password is not correct return apology
        if  user is not None:
            print('a')
            if not check_password_hash(user["password"],password):
                return apology("Invaid password")
        else:
            print('b')
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

@app.route("/logout")
def logout():
    session.clear() #clears the current session as user has logged out
    return redirect("/login") 

@app.route("/credits")
def credits():
    return render_template("credits.html")

# student functions

@login_required #decorater which requires user to be logged in to view
@app.route('/viewjobs', methods = ["GET", "POST"])
def view_jobs():
    conn = get_db()
    cursor1 = conn.cursor()#cursor 1 interacts with the jobs table
    cursor2 = conn.cursor()#cursor 2 interacts with the intrested_jobs table

    #select all jobs the user has applied to and store it in array
    interested_jobs_cursor = cursor2.execute("SELECT * FROM intrested_jobs WHERE user_id = ?", (session["user_id"], ))
    interested_jobs = []
    for interested_job in interested_jobs_cursor:
        print(interested_job)
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
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #sends the file path when called in the html
    return send_from_directory(app.config['UPLOAD_PATH'], filename, mimetype='application/pdf')


@login_required
@app.route('/pinnedjobs', methods = ["GET", "POST"])
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
    



#employer functions


@login_required
@app.route("/myjobs", methods = ["GET", "POST"])
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
@app.route("/applications")
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
    
        
    
    



#admin functions
@login_required
@app.route("/reviewJobs", methods = ["GET","POST"])
def reviewJobs():

    conn = get_db()
    cursor = conn.cursor()

    #select all jobs 
    jobs = cursor.execute("SELECT * FROM jobs")
    portfolio=[]

    for job in jobs:
        #if a job has not already been approved send them to the admin to review
        if job["status"]!="approved":
            portfolio.append({"company":job["company"], "id":job["id"],"company_role":job["company_role"],"pay":job["pay"], "Description": job["Description"]})
    

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
            
        return redirect("/reviewJobs")
    

    conn.close()
    return render_template("areview_jobs.html", portfolio = portfolio)

@login_required
@app.route("/reviewprofiles", methods = ["GET", "POST"])
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
        print("Portfolio:",portfolio)
    if request.method == "POST":
        decision = request.form.get("action")
        if decision:
            action, job_id = decision.split("_")
            job_id = int(job_id)
            if action == "approve":
                #if the user is approved, set their status to that
                cursor.execute("UPDATE students SET status = ?", ("approved",))
            if action == "decline":
                #if they are declined, delete them from the table
                cursor.execute("DELETE FROM students WHERE id = ?",(job_id,))
        conn.commit()
        conn.close()
        return redirect("/")
    conn.close()
    return render_template("aprofiles.html", portfolio = portfolio)

@login_required
@app.route("/reviewapplicants", methods = ["GET", "POST"])
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
        return redirect("/reviewapplicants")
    conn.close()
    return render_template("aapplications.html", portfolio = portfolio)

    
    

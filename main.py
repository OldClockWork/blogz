from flask import request, redirect, render_template, flash, session
from app import app, db
from models import User, Blog #Tables
import html


#--------LOGIN
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

#--------LOGIN CONFIRMATION
@app.route("/logConfirm", methods=["POST"])
def login_confirm():
    
    email = request.form["email"]
    password = request.form["password"]

    users = User.query.filter_by(email=email)
    password_check = User.query.filter_by(password=password).first() # TODO Fix

    error = ""

    if(users.count() == 1): #TODO Needs a proper password check.
        session['user'] = email
        return redirect("/")
    else:
        error = "Error: Email doesn't exist or incorrect password."
        return render_template("login.html", error=error)


#--------LOGOUT
@app.route("/logout", methods=["POST"])
def logout():
    del session["user"]
    return redirect("/")


#--------REGISTER
@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

#--------REGISTER CONFIRMATION
@app.route("/regConfirm", methods=["POST"])
def reg_confirm():

    name = request.form["user_name"]
    email = request.form["email"]
    password = request.form["password"]
    repassword = request.form["re-password"]
    error = ""
    email_check = User.query.filter_by(email=email).count() #Counts any email that is the same attempting to be registered.
    name_check = User.query.filter_by(name=name).count()

    if(email.strip()=="" or password.strip()=="" or password != repassword or name.strip()==""):
        error = "Error: Textfields can not be left empty or password validation did not match!"
        return render_template("register.html", error=error)
    
    elif(email_check > 0):
        error = "Error: Email already exists!"
        return render_template("register.html", error=error)
    
    elif(name_check > 0):
        error = "Error: Name taken!"
        return render_template("register.html", error=error)
    
    else:
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session["user"] = user.email #Places the user within the session as their email.
        return redirect("/")

#-------OPEN PROFILE
@app.route("/profile_select", methods=["GET"])
def profile_focus():

    id = request.args.get("id")
    profile = User.query.get(int(id))
    blogs = Blog.query.filter_by(owner_id = profile.id).all()
    return render_template("profile_page.html", blogs=blogs)


#-------POST FOCUS
@app.route("/focus_post", methods=["GET"])
def post_focus():

    id = request.args.get("id")  
    entry = Blog.query.get(int(id))
    user = User.query.filter_by(id = entry.owner_id).first()
    return render_template("focus_post.html", title=entry.title, body=entry.body, id=entry.owner_id, user=user.name)


#-------POST CREATION
@app.route("/create_post", methods=["GET"])
def post_create():
    return render_template("postCreate.html")

#-------ADDS NEW POST
@app.route("/new_post", methods=["POST"])
def new_post():
    title = request.form["title"]
    body = request.form["body"]
    user = User.query.filter_by(email = session['user']).first()

    post = Blog(title=title, body=body, owner=user)
    db.session.add(post)
    db.session.commit()
    return render_template("postConfirm.html")

#-------MAIN PAGE
@app.route("/", methods=["POST", "GET"])
def index():
    profiles = User.query.filter_by().all()
    return render_template("current_profiles.html", profiles=profiles)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU' #Needed in order for the session to work.

if __name__ == "__main__":
    app.run()
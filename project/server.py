from flask import Flask, render_template, request, abort, session, flash, redirect
from base import app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def index():
    return render_template("index.html", session = session)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def handle_login():
    username = request.form["username"]
    password = request.form["password"]

    user_from_db = User.query.filter(User.username == username).first()

    # User doesn't exist in the DB
    if user_from_db is None:
        flash("wrong user or password")
        return render_template("login.html")
    else:
        # user exists, and the password is correct!
        if check_password_hash(user_from_db.password, generate_password_hash(password)):
            session["username"] = username
        # user exists, but the password is incorrect
        else:
            flash("wrong user or password")
            return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def handle_signup():
    username = request.form["username"]
    password = request.form["password"]

    user_from_db = User.query.filter(User.username == username).first()

    if user_from_db is not None:
        flash("username already exists")
        render("signup.html")
    else:
        hashed_pass = generate_password_hash(password)
        user = User(username = username, password = hashed_pass)

        # save the user in the DB.  This will execute an insert statement to our database
        db.session.add(user)
        db.session.commit()

        # save in the session the username of the user
        session["username"] = username

        return redirect("/")


app.run(debug = True)

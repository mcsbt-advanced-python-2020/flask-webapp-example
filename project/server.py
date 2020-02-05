from flask import Flask, render_template, request, abort, session, flash, redirect
from base import app, db
from models import User, Tweet
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def index():

    query = Tweet.query

    if "username" in session:
        user = User.query.filter(User.username == session["username"]).first()
        query = query.filter(Tweet.user_id == user.id)

    tweets = query.all()

    return render_template("index.html", session = session, tweets = tweets)

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

@app.route("/tweet", methods=["POST"])
def handle_tweet():
    message = request.form["tweet"]

    user = User.query.filter(User.username == session["username"]).first()
    tweet = Tweet(user = user, text = message)

    db.session.add(tweet)
    db.session.commit()

    return redirect("/")

@app.route("/<username>")
def profile(username):
    user = User.query.filter(User.username == username).first_or_404()

    return render_template("user.html", session = session, user = user)

app.run(debug = True)

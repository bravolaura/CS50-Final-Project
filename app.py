import os
import datetime
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show emails"""
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = user[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE recipient = ?", username)
    return render_template("index.html", emails=emails)

@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    """Compose"""
    if request.method == "GET":
        # Render compose.html
        userId = session["user_id"]
        senderDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
        sender = senderDB[0]["username"]
        return render_template("compose.html", sender=sender)

    else:
        # Update emails table
        sender = request.form.get("sender")
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")

        if not sender or not body or not subject or not recipient:
            return apology("Can not be empty", 406)

        # Update emails table
        db.execute("INSERT INTO emails (sender, recipient,subject,body) VALUES (?,?,?,?)",
                    sender, recipient, subject, body)

        return redirect("/sent")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username").lower():
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").lower())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/sent")
@login_required
def sent():
    """Display sent."""
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    sender = username[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE sender = ?", sender)
    return render_template("sent.html", emails = emails)

@app.route("/email", methods=["POST"])
@login_required
def email():
    """View email details"""
    if request.method == "POST":
        emailId = request.form.get("emailId")
        email = db.execute("SELECT * FROM emails WHERE id = ?", emailId)
        email = email[0]
        return render_template("email.html", email = email)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        # Redirect user to register
        return render_template("register.html")

    else:
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Query database for username and check if username or useremail already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return apology("Username already exists", 400)

        # Ensure password was submitted, and it's 8 characters long, has a number
        elif not password:
            return apology("must provide password", 400)
        elif len(password) < 8:
            return apology("Password must be at least 8 characters length", 400)
        elif re.search('[0-9]', password) is None:
            return apology("Make sure your password has a number in it", 400)

        # Ensure password confirmation was submitted
        elif not confirmation:
            return apology("must provide password confirmation", 400)

        # Validate password and password confirmation are the same
        if password != confirmation:
            return apology("Password must match", 400)

        # Hash password to add it into users table
        hash = generate_password_hash(password)

        # Add the username and password to users table
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Query database for username and check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

@app.route("/reply", methods=["POST"])
@login_required
def reply():
    """reply"""
    if request.method == "POST":
        # Returns email
        emailId = request.form.get("emailId")
        email = db.execute("SELECT * FROM emails WHERE id = ?", emailId)
        email = email[0]
        return render_template("reply.html", email=email)

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """View email details"""
    if request.method == "POST":
        # Get the email Id from html
        emailId = request.form.get("emailId")
        # Update emails table
        db.execute("DELETE FROM emails WHERE id = ?", emailId)
        return redirect("/")
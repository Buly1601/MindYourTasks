import os
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/main")
def main():
    """
    Returns the main page of the app, where basic info and options as well as contact
    is provided 
    """
    return render_template("index.html", title="Intro Screen", url=os.getenv("URL"))

@app.route("/login", methods=["POST"])
def login():
    #TODO

    return render_template("login.html", title="Login", url=os.getenv("URL"))

@app.route("/register", methods=["POST"])
def register():
    #TODO

    return render_template("register.html", title="Register", url=os.getenv("URL"))

@app.route("/health")
def healthy():
    return "Healthy as it should."

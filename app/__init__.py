import os
import sqlite3
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

app = Flask(__name__)

db.init_app(app)
app.config["DATABASE"] = os.path.join(os.getcwd(), "flask.sqlite")

with app.app_context():

    @app.route("/")
    def main():
        """
        Returns the main page of the app, where basic info and options as well as contact
        is provided 
        """
        return render_template("index.html", title="Intro Screen", url=os.getenv("URL"))

    def error_caller(error):
        """
        Reusage function to recycle code
        """
        if error == "username":
            return "Username is required."
        elif error == "password":
            return "Password is required."
        elif error == "confPassword":
            return "Passwords must match."

    @app.route("/register", methods=["GET","POST"])
    def register():
        """
        Regiters into db the new user with username and  hashes with sha-21 the password
        """
        if request.method == "POST":
            dab = db.get_db() 
            username = request.form.get("username")
            password = request.form.get("password")
            confPassword = request.form.get("confPassword")
            
            
            print(confPassword)
            error = None

            if not username:
                error = error_caller("username")
            elif not password:
                error = error_caller("password")
            if password != confPassword:
                error = error_caller("confPassword")
            elif dab.execute(
                "SELECT * FROM user_info WHERE Username = ?", (username,)
            ).fetchone() != None:
                error = "Username already exists"

            if error == None:
                dab.execute(
                    "INSERT INTO user_info (Username, Password) VALUES (?, ?)",
                    (username, generate_password_hash(password),))
                dab.commit()

                return f"User {username} created successfully"

            else:
                return error, 418

        else:
            return render_template("register.html", title="Register", url=os.getenv("URL"))

    @app.route("/login", methods=["GET","POST"])
    def login():
        """
        Checks for input and when given, checks for the information in the database
        """
        if request.method == "POST":
            dab = db.get_db()
            username = request.form.get("username")
            password = request.form.get("password")        
            error = None
            
            if not username:
                error = error_caller("username")
            elif not password:
                error = error_caller("password")

            # check for the user in the database
            user_ = dab.execute(
                "SELECT * FROM user_info WHERE Username = ?", (username,)
            ).fetchone()

            if not user_:
                error = "Nonexistent or incorrect username"
            elif not check_password_hash(user_["Password"],password):
                error = "Incorrect password"

            if error:
                return error, 418
        
            return "Login successfull"

        else:
            return render_template("login.html", title="Login", url=os.getenv("URL"))

    @app.route("/health")
    def healthy():
        """
        Health function for life checking
        """
        return "Healthy as it should."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=False)

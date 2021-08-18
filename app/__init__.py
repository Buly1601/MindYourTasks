import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config["DATABASE"] = os.path.join(os.getcwd(), "flask.sqlite")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

"""class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #owner = d.Column(d.Text, nullable=False)
    def __init__(self, content, owner):
        self.content = content
        self.done = False
        self.owner = owner
    def __repr__(self):
        return '<Content %s>' % self.owner
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    level = db.Column(db.Integer)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    health = db.Column(db.Integer)
    hunger = db.Column(db.Integer)
    point = db.Column(db.Integer)
    #tasks_id = db.Column(db.ForeignKey(Task.id))
   # tasks = db.relationship(Task, backref='owner')
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.level = 0
        self.hunger = 100
        self.health = 100
        self.point = 0
        self.name = "hi"
        self.type = "cat"
    def __repr__(self):
        return f"<User {self.username}>"
"""


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # owner = d.Column(d.Text, nullable=False)

    def __init__(self, content, owner):
        self.content = content
        self.done = False
        self.owner = owner

    def __repr__(self):
        return "<Content %s>" % self.owner


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    level = db.Column(db.Integer)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    health = db.Column(db.Integer)
    hunger = db.Column(db.Integer)
    point = db.Column(db.Integer)
    # tasks_id = db.Column(db.ForeignKey(Task.id))
    tasks = db.relationship(Task, backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.level = 0
        self.name = "Pretzel"
        self.type = "cat"
        self.hunger = 100
        self.health = 100
        self.point = 0

    def __repr__(self):
        return f"<User {self.username}>"


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

    @app.route("/register", methods=["GET", "POST"])
    def register():
        """
        Regiters into db the new user with username and  hashes with sha-21 the password
        """

        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            confPassword = request.form.get("confPassword")
            error = None

            print(username, password, confPassword)

            if not username:
                error = error_caller("username")
            elif not password:
                error = error_caller("password")
            if password != confPassword:
                error = error_caller("confPassword")
            elif User.query.filter_by(username=username).first() is not None:
                error = f"User {username} already exists"
                print(error, "ALL CLEAR HERE---")

            if error is None:
                new_username = User(username, generate_password_hash(password))
                db.session.add(new_username)
                db.session.commit()

                # return f"User {username} created successfully"

                return redirect(url_for("login"))

            else:
                flash(error)
                return render_template(
                    "register.html", title="Register", url=os.getenv("URL")
                )

        else:
            return render_template(
                "register.html", title="Register", url=os.getenv("URL")
            )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """
        Checks for input and when given, checks for the information in the database
        """
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            error = None

            if not username:
                error = error_caller("username")
            elif not password:
                error = error_caller("password")

            # check for the user in the database
            user_ = User.query.filter_by(username=username).first()

            if not user_:
                error = "Nonexistent or incorrect username"
            elif not check_password_hash(user_.password, password):
                error = "Incorrect password"

            if error:
                flash(error)
                return render_template(
                    "login.html", title="Login", url=os.getenv("URL")
                )
            session["username"] = username

            return redirect(url_for("todo"))

        else:
            return render_template("login.html", title="Login", url=os.getenv("URL"))

    @app.route("/health")
    def healthy():
        """
        Health function for life checking
        """
        return "Healthy as it should."

    @app.route("/logout")
    def logout():
        del session["username"]
        return redirect("/")

    @app.route("/todo", methods=["GET", "POST"])
    def todo():
        """
        Health function for life checking
        """

        username = session["username"]
        owner = User.query.filter_by(username=username).first()

        # tasks = Task.query.filter_by(done=False, owner=owner).all()
        tasks = Task.query.filter_by(owner=owner).all()
        completed_tasks = Task.query.filter_by(done=True, owner=owner).all()
        tasks = Task.query.all()

        attributes = {
            "Health": owner.health,
            "Hunger": owner.hunger,
            "Level": owner.level,
        }

        return render_template("todo.html", url=os.getenv("URL"))

    @app.route("/task", methods=["POST"])
    def add_task():
        content = request.form["content"]
        if not content:
            return "Error"

        username = session["username"]
        owner = User.query.filter_by(username=username).first()
        new_task = Task(content, owner)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("todo"))

    @app.route("/delete/<int:task_id>")
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return redirect("/")

        db.session.delete(task)
        db.session.commit()

        return redirect(url_for("todo"))

    @app.route("/done/<int:task_id>")
    def resolve_task(task_id):
        task = Task.query.get(task_id)

        if not task:
            return redirect("/")
        if task.done:
            task.done = False
        # after resolving add points to the user
        else:
            task.done = True

        db.session.commit()

        return redirect(url_for("todo"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=False)

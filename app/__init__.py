import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
from flask import Flask, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, todo_helper
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

db.init_app(app)
app.config["DATABASE"] = os.path.join(os.getcwd(), "flask.sqlite")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///b.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

d = SQLAlchemy(app)

class Task(d.Model):
    id = d.Column(d.Integer, primary_key=True)
    content = d.Column(d.Text)
    done = d.Column(d.Boolean, default=False)
    owner_id = d.Column(d.Integer, d.ForeignKey('user.id'))
    #owner = d.Column(d.Text, nullable=False)

    def __init__(self, content, owner):
        self.content = content
        self.done = False
        self.owner = owner

    def __repr__(self):
        return '<Content %s>' % self.owner

class User(d.Model):

    id = d.Column(d.Integer, primary_key=True)
    username = d.Column(d.String(120))
    password = d.Column(d.String(120))
    tasks = d.relationship('Task', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    '''def __repr__(self):
        return '<User %r>' % self.username'''

d.create_all()

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
            dab = db.get_db()
            username = request.form.get("username")
            password = request.form.get("password")
            confPassword = request.form.get("confPassword")

            



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
                new_user = User(username, password)
                d.session.add(new_user)
                d.session.commit()

                return redirect(url_for('login'))
            else:
                flash(error)
                return render_template("register.html", title="Register", url=os.getenv("URL"))

        else:
            return render_template("register.html", title="Register", url=os.getenv("URL"))


    @app.route("/login", methods=["GET", "POST"])
    def login():
        """
        Checks for input and when given, checks for the information in the database
        """
        if request.method == "POST":
            dab = db.get_db()
            username = request.form.get("username")
            password = request.form.get("password")
            error = None

            #user = User.query.filter_by(username=username).first()
            '''if user and user.password == password:
                session['username'] = username
                flash("Logged in")
                return redirect(url_for('todo'))'''

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
            elif not check_password_hash(user_["Password"], password):
                error = "Incorrect password"

            if error:
                flash(error)
                return render_template("login.html", title="Login", url=os.getenv("URL"))

            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session['username'] = username
                flash("Logged in")
                #return redirect(url_for('todo'))
            #session['username'] = username

            return redirect(url_for('todo'))

        else:
            return render_template("login.html", title="Login", url=os.getenv("URL"))


    @app.route('/logout')
    def logout():
        del session['username']
        return redirect('/')

    @app.route("/health")
    def healthy():
        """
        Health function for life checking
        """
        return "Healthy as it should."


    @app.route("/todo", methods=["GET", "POST"])
    def todo():
        """
        Health function for life checking
        """

        username = session['username']
        owner = User.query.filter_by(username=username).first()
        #owner = User.query.filter_by(username=session['username']).first()

        tasks = Task.query.filter_by(done=False, owner=owner).all()
        completed_tasks = Task.query.filter_by(done=True, owner=owner).all()
        #tasks = Task.query.all()
        return render_template('todo.html', tasks=tasks, completed_tasks=completed_tasks, url=os.getenv("URL"))



    '''@app.route('/todo', methods=['POST', 'GET'])
    def todo():
        dab = db.get_db()
        username = session['username']
        #owner = User.query.filter_by(email=session['username']).first()

        if request.method == 'POST':
            task_name = request.form['content']
            new_task = Task(task_name, username)
            print(username)
            d.session.add(new_task)
            d.session.commit()

        tasks = Task.query.filter_by(done=False, owner=username).all()
        completed_tasks = Task.query.filter_by(done=True, owner=username).all()
        return render_template('todo.html', title="Get It Done!",
                               tasks=tasks, completed_tasks=completed_tasks)'''

'''----------------------------------------------------------'''

@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    username = session['username']
    owner = User.query.filter_by(username=username).first()
    new_task = Task(content, owner)
    d.session.add(new_task)
    d.session.commit()

    '''task = Task(content, username)
    d.session.add(task)
    d.session.commit()'''
    return redirect(url_for('todo'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    d.session.delete(task)
    d.session.commit()
    return redirect(url_for('todo'))


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    d.session.commit()
    return redirect(url_for('todo'))


'''----------------------------------------------------------'''

'''

    @app.route('/item/new', methods=['POST'])
    def add_item():
        # Get item from the POST body
        req_data = request.get_json()
        item = req_data['item']

        # Add item to the list
        res_data = todo_helper.add_to_list(item)

        # Return error if item not added
        if res_data is None:
            response = Response("{'error': 'Item not added - '}" + item, status=400, mimetype='application/json')
            return response

        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')

        return response


    @app.route('/items/all')
    def get_all_items():
        # Get items from the helper
        res_data = todo_helper.get_all_items()
        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')
        return response


    @app.route('/item/status', methods=['GET'])
    def get_item():
        # Get parameter from the URL
        item_name = request.args.get('name')

        # Get items from the helper
        status = todo_helper.get_item(item_name)

        # Return 404 if item not found
        if status is None:
            response = Response("{'error': 'Item Not Found - '}" + item_name, status=404, mimetype='application/json')
            return response

        # Return status
        res_data = {
            'status': status
        }

        response = Response(json.dumps(res_data), status=200, mimetype='application/json')
        return response


    @app.route('/item/update', methods=['PUT'])
    def update_status():
        # Get item from the POST body
        req_data = request.get_json()
        item = req_data['item']
        status = req_data['status']

        # Update item in the list
        res_data = todo_helper.update_status(item, status)
        if res_data is None:
            response = Response("{'error': 'Error updating item - '" + item + ", " + status + "}", status=400,
                                mimetype='application/json')
            return response

        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')

        return response


    @app.route('/item/remove', methods=['DELETE'])
    def delete_item():
        # Get item from the POST body
        req_data = request.get_json()
        item = req_data['item']

        # Delete item from the list
        res_data = todo_helper.delete_item(item)
        if res_data is None:
            response = Response("{'error': 'Error deleting item - '" + item + "}", status=400,
                                mimetype='application/json')
            return response

        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')

        return response

'''

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=False)
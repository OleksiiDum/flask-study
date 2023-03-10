from flask import Flask, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import hashlib


app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

salt = "saltedhash"

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key = True)
    todo = db.Column(db.String())
    description = db.Column(db.String())
    important = db.Column(db.String())
    done = db.Column(db.Boolean, default=False)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

with app.app_context():
    db.create_all()

@app.route('/')
def main():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/all_todos', methods=['POST', 'GET'])
def all_todos():
    if  request.method == "POST":
        todo = request.get_json()["todo"]
        description = request.get_json()["description"]
        db_todo = Todo(todo=todo, description=description)
        db.session.add(db_todo)
        db.session.commit()
        return jsonify({"Added": f"{todo}"})
    elif request.method == "GET":
        todos = Todo.query.all()
        json_todos = []
        for todo in todos:
            todo_dict = {"todo": todo.todo, "description": todo.description}
            json_todos.append(todo_dict)
        return jsonify({"todos": json_todos})
    
@app.route('/todo/<id>', methods=['DELETE', 'GET'])
def todo_id(id):
    if request.method == "GET":
        get_todo = Todo.query.get(id)
        return jsonify({"todo": get_todo.todo, "description": get_todo.description})
    elif request.method == "DELETE":
        get_todo = Todo.query.get(id)
        db.session.delete(get_todo)
        db.session.commit()
        return jsonify({"Deleted": f"{get_todo.todo}"})

@app.route('/registration', methods=['POST'])
def register():
    if request.method == "POST":
        user = request.get_json()["username"]
        salted_password = request.get_json()["password"] + salt
        hashed = hashlib.md5(salted_password.encode())
        db_todo = User(username=user, password=hashed.hexdigest())
        db.session.add(db_todo)
        db.session.commit()
        return jsonify({"Added": f"{user}: {hashed.hexdigest()}"})

@app.route('/login', methods=['GET'])
def login():
    if request.method == "GET":
        user = request.get_json()["username"]
        print(user)
        salted_password = request.get_json()["password"] + salt
        hashed = hashlib.md5(salted_password.encode())
        db_user = User.query.filter_by(username=user).first()
        if db_user:
            if hashed.hexdigest() == db_user.password:
                return jsonify({"User": f"{db_user.username} is logged in"})
            else:
                return jsonify({"Error": "Password is incorrect"})
        else:
            return jsonify({"Error": "User not found"})


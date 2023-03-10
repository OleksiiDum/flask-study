from flask import Flask, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key = True)
    todo = db.Column(db.String())
    description = db.Column(db.String())
    important = db.Column(db.String())
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def main():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/all_todos', methods=['POST', 'GET'])
def all_todos():
    if  request.method == "POST":
        todo = request.form["todo"]
        description = request.form["description"]
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
def todo_id():
    if request.method == "GET":
        todo = request.args.get('todo')
        get_todo = Todo.query.get(todo)
        return jsonify({"todo": get_todo.todo, "description": get_todo.description})
    elif request.method == "DELETE":
        todo = request.form["todo"]
        get_todo = Todo.query.get(todo)
        db.session.delete(get_todo)
        db.session.commit()
        return jsonify({"Deleted": f"{get_todo.todo}"})


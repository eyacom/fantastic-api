from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields as FM
from sqlalchemy import (Text)  # you can add another table column type if you need
from flask_migrate import Migrate

# THIS CODE IS DERIVATED FROM THE EXAMPLE OF Flask-RESTX EXTENSION

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='TodoMVC API',
    description='A simple TodoMVC API with Flask and SQLAlchemy',
)

ns = api.namespace('todos', description='TODO operations')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)
todo = api.model(
    'Todo', {
        'id':
        fields.Integer(readOnly=True,
                       description='The task unique identifier'),
        'task':
        fields.String(required=True, description='The task details')
    })


class TodoDAO(db.Model):
    __tablename__ = 'todo'
    id =db.Column(db.Integer,primary_key=True)
    task=db.Column(Text)
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        todo=TodoDAO.query.filter_by(id=id).first()
        if todo is not None:
            return todo
        api.abort(404, "Todo {} doesn't exist".format(id))
    def create(self, data):
        todo=TodoDAO()
        todo.task = data['task']
        todo.id = self.counter = self.counter + 1
        self.todos.append(todo.task)
        db.session.add(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.task=data
        return todo

    def delete(self, id):
        todo = self.get(id)
        db.session.delete(todo)
        self.todos.remove(todo.task)

class TaskSchema(Schema):
    id=FM.Int()
    task=FM.Str()
db.configure_mappers()
db.create_all()

schema=TaskSchema()

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return TodoDAO.query.all()

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        payload = request.get_json()
        todo= TodoDAO()
        todo.id = payload['id']
        todo.task=payload['task']
        db.session.add(todo)
        db.session.commit()
        return {
            "data": schema.dump(todo)
        }


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return TodoDAO.query.filter_by(id=id).first()

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        todo=TodoDAO.query.filter_by(id=id).first()
        db.session.delete(todo)
        db.session.commit()
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self,id):
        '''Update a task given its identifier'''
        data=api.payload['task']
        todo=TodoDAO.query.filter_by(id=id).first()
        todo.task=data
        db.session.add(todo)
        db.session.commit()
        return {
            "status": "Updated task with id " + str(id)
        }
        
if __name__ == '__main__':
    app.run(debug=True)

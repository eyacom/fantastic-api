from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Todos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# THIS CODE IS DERIVATED FROM THE EXAMPLE OF Flask-RESTX EXTENSION

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

api = Api(
    app,
    version='1.0',
    title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model(
    'Todo', {
        'id':
        fields.Integer(readOnly=True,
                       description='The task unique identifier'),
         'createdAt':
        fields.DateTime(readOnly=True,
                        description='datetime value of task creation time'),

        'task':
        fields.String(required=True, description='The task details')
    })
class TodoTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(140))
    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
            return d
    def __repr__(self):
        return row2dict(self)

class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        todo = TodoTask.query.filter_by(id=id).first()

            # TODO : Improve the searching complexity to O(1) using hashmap structure
        return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        new = TodoTask(task=todo['task'])
        db.session.add(new)
        db.session.commit()
        return todo

    def update(self, id, data):
        todo = TodoTask.query.filter_by(id=id).first()
        todo.task = data['task']
        db.session.commit()
        return todo

    def delete(self, id):
        todo = TodoTask.query.filter_by(id=id).first() 
        db.session.delete(todo)  
        db.session.commit()
    def listAll(self):
        return TodoTask.query.all()


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.listAll()

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)

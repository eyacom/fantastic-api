from flask import Flask
from flask_restx import Api, Resource, fields
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# THIS CODE IS DERIVATED FROM THE EXAMPLE OF Flask-RESTX EXTENSION

app = Flask(__name__)

# DataBase configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# Initialise db
db = SQLAlchemy(app)


# create the schema of db
class DBModel (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.DateTime, default=datetime.now())
    task = db.Column(db.String(80),  nullable=False)


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


class TodoDAO(object):
    def __init__(self):
        self.counter = 0

    def get(self, id):
        # searching for the wanted task
        todo = DBModel.query.filter_by(id=id).first()
        if todo is not None:
            # Convert sqlalchemy row object to python dict
            todo_d = todo.__dict__
            # remove the sqlalchemy extra data
            todo_d.pop('_sa_instance_state', None)
            return todo_d
        api.abort(404, "Todo {} doesn't exist".format(id))

    def getAll(self):
        # query all db
        todos = DBModel.query.all()
        return todos

    def create(self, data):
        todo_d = {}
        todo_d['id'] = self.counter = self.counter + 1
        todo_d['createdAt'] = datetime.now()
        todo_d['task'] = data['task']
        todo = DBModel(id=todo_d['id'], createdAt=todo_d['createdAt'], task=todo_d['task'])
        db.session.add(todo)
        db.session.commit()
        return todo_d

    def update(self, id, data):
        # searching for the wanted task
        todo = DBModel.query.filter_by(id=id).first()
        if todo is not None:
            # Convert sqlalchemy row object to python dict
            todo_d = todo.__dict__
            # remove the sqlalchemy extra data
            todo_d.pop('_sa_instance_state', None)
            todo_d['task'] = data['task']
            db.session.commit()
            return todo_d
        api.abort(404, "Todo {} doesn't exist".format(id))

    def delete(self, id):
        # search for the task
        todo = DBModel.query.filter_by(id=id).first()
        if todo is not None:
            # This will let us Delete the task
            db.session.delete(todo)
            db.session.commit()
        else:
            api.abort(404, "Todo {} doesn't exist".format(id))


DAO = TodoDAO()


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.getAll()

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

from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

# THIS CODE IS DERIVATED FROM THE EXAMPLE OF Flask-RESTX EXTENSION

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\\fantastic-api\\bd.db'
db = SQLAlchemy(app)

api = Api(
    app,
    version='1.0',
    title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')


class TodoDB(db.Model):
        # __tablename__ = 'todos'
        id_t = db.Column('id_t', db.Integer, primary_key=True)
        task = db.Column('task', db.String(300))


class TodoDAO(object):
    def get(self, id):
        todo = TodoDB.query.filter_by(id_t=id)
        return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def get_all(self):
        todo = TodoDB.query.all()
        return todo

    def create(self, data):
        todo_task = data['task']
        todo_id = TodoDB.query.count() + 1
        todo = TodoDB(todo_id, todo_task)
        db.session.add(todo)
        db.session.commit()
        return todo

    def update(self, id, data):
        todo = TodoDB.query.filter_by(id_t=id)
        todo.task = data['task']
        db.session.commit()
        return todo

    def delete(self, id):
        todo = TodoDB.query.filter_by(id_t=id)
        db.session.delete(todo)
        db.session.commit()

DAO = TodoDAO()


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    # @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.get_all()

    @ns.doc('create_todo')
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    # @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)

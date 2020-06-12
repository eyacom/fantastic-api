from flask import Flask
from flask_restx import Api, Resource, fields
from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


# THIS CODE IS DERIVATED FROM THE EXAMPLE OF Flask-RESTX EXTENSION

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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


   

class TodoDAO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.String(120), unique=True)
     task = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)



    def __init__(self,counter,todos):
        self.counter = 0
        self.todos = []
        
   def __repr__(self):
       
rep =TodoDAO.query.all()
return rep



    def get(self, id):
        for todo in self.todos:
            # TODO : Improve the searching complexity to O(1) using hashmap structure
            todo = TodoDAO.query.filter_by(id='id').first()
            if todo['id'] == id:
                
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = TodoDAO(task= data['task'])
        db.session.add(todo)
        db.session.commit()
        return todo
    

    def update(self, id, data):
        todo = TodoDAO.query.filter_by(id=id).first()  
        todo.task = data['task']    
        db.session.commit()
        return todo
        
        

    def delete(self, id):
        
        todo = TodoDAO.query.filter_by(id=id).first()        
        db.session.delete(todo)  
        db.session.commit()


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
        return DAO.todos

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

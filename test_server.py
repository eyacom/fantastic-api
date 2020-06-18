from server import TodoDAO


def test_list_todo():
    DAO = TodoDAO()
    t1 = DAO.create({'task': 'test-todo'})
    assert t1 is not None
    assert t1['id'] > 0
    t2 = DAO.get(t1['id'])
    assert t2 is not None
    assert t2 == t1['task']
    assert t1['createdAt'] is not None


def test_empty_todo():
    DAO = TodoDAO()
    assert len(DAO.todos) == 0


def test_notfound_todo():
    DAO = TodoDAO()
    empty_task = DAO.create({'task': ''})
    if empty_task is None:
        raise TypeError

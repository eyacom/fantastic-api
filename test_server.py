from server import TodoDAO


def test_list_todo():
    DAO = TodoDAO()
    t1 = DAO.create({'task': 'test-todo'})
    assert t1 is not None
    assert t1['id'] > 0
    t2 = DAO.get(t1['id'])[1]
    assert t2 is not None
    assert t2['task'] == t1['task']


def test_empty_todo():
    DAO = TodoDAO()
    assert len(DAO.todos) == 0


# TODO : add test raise exception when task is absent
def test_notfound_todo():
    DAO=TodoDAO()
    t11=DAO.create({'task':'test-notfound1'})
    t22=DAO.create({'task':'test-notfound2'})
    with pytest.raise(Exception):
        t3=DAO.get(3)
    pass

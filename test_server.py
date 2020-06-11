from server import TodoDAO


def test_list_todo():
    DAO = TodoDAO()
    t1 = DAO.create({'task': 'test-todo'})
    assert t1 is not None
    key_t1 = DAO.todos.copy().popitem()[0]
    assert key_t1 > 0
    t2 = DAO.get(key_t1)
    assert t2 is not None
    assert t2 == t1


def test_empty_todo():
    DAO = TodoDAO()
    assert len(DAO.todos) == 0


# TODO : add test raise exception when task is absent
def test_notfound_todo():
    pass

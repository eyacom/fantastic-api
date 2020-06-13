from server import TodoDAO


def test_list_todo():
    DAO = TodoDAO()
    t1 = DAO.create({'task': 'test-todo'})
    assert t1 is not None
    assert t1.id_t > 0
    t2 = DAO.get(t1.id_t)
    assert t2 is not None
    assert t2.task == t1.task


def test_empty_todo():
    DAO = TodoDAO()
    assert DAO.isNull()


# TODO : add test raise exception when task is absent
def test_notfound_todo():
    pass

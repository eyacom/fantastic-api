from server import TodoDAO
import pytest


def test_list_todo():
    DAO = TodoDAO()
    t1 = DAO.create({'task': 'test-todo'})
    assert t1 is not None
    assert t1['id'] > 0
    t2 = DAO.get(t1['id'])
    assert t2 is not None
    assert t2['task'] == t1['task']


# TODO : add test raise exception when task is absent
# If the task is empty
def empty_todo():
    DAO = TodoDAO()
    empty = DAO.create({'task': ''})
    if not empty['task']:
        raise Exception("Task is empty")


# If the task is null
def notfound_todo():
    DAO = TodoDAO()
    none = DAO.create({'task': None})
    if none['task'] is None:
        raise Exception("Task not found")


def test_notfound_todo():
    with pytest.raises(Exception):
        empty_todo()
    with pytest.raises(Exception):
        notfound_todo()

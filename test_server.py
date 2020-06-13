from server import TodoDAO
import pytest


def test_list_todo():
    DAO = TodoDAO()
    t1 = DAO.create({'task': 'test-todo'})
    assert t1 is not None
    assert t1.id_t > 0
    t2 = DAO.get(t1.id_t)
    assert t2 is not None
    assert t2.task == t1.task


# Function to check if the task is empty or not
def empty_todo():
    DAO = TodoDAO()
    t = DAO.create(0)
    if t.task == '':
        raise Exception("Task is empty")


# Function to check if the task is found or not
def notfound_todo():
    DAO = TodoDAO()
    t = DAO.create({'task': None})
    if t.task is None:
        raise Exception("Task not found")


# Test raise exception when task is absent added
def test_notfound_todo():
    with pytest.raises(Exception):
        notfound_todo()
    with pytest.raises(Exception):
        empty_todo()

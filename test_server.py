from server import TodoDAO
import pytest


def test_list_todo():
    DAO = TodoDAO()
    t1 = DAO.create({'task': 'test-todo'})
    assert t1 is not None
    assert t1.id > 0
    t2 = DAO.get(t1.id)
    assert t2 is not None
    assert t2.task == t1.task
    assert t2.createdAt is not None


def test_empty_todo():
    DAO = TodoDAO()
    assert len(DAO.todos) == 0


class TaskNotFoundException(Exception):
    pass


def empty_task():
    DAO = TodoDAO()
    t = DAO.create({'task': ''})
    # If the task is empty
    if not t['task']:
        raise TaskNotFoundException("Exception TaskNotFound raised")


def none_task():
    DAO = TodoDAO()
    t2 = DAO.create({'task': None})
    # If the task is null
    if t2['task'] is None:
        raise AssertionError("Invalid null task!")


def test_notfound_todo():
    with pytest.raises(TaskNotFoundException):
        empty_task()
    with pytest.raises(AssertionError):
        none_task()

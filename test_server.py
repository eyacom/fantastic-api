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
    # we test that our Db is not empty
    DAO = TodoDAO()
    assert len(DAO.getAll()) != 0


def check_empty_task():
    DAO = TodoDAO()
    t1 = DAO.create({'task': None})
    if not t1.task:
        raise Exception("Task is absent Exception (None found)")


def check_none_task():
    DAO = TodoDAO()
    t2 = DAO.create({'task': ''})
    if t2.task == "":
        raise Exception("Task is absent Exception raised (Empty String)")


def check_notfound_task():
    DAO = TodoDAO()
    t3 = DAO.create({})
    if 'task' not in t3:
        raise Exception("Task not Found Exception")


def test_notfound_todo():
    with pytest.raises(Exception):
        check_empty_task()
    with pytest.raises(Exception):
        check_none_task()
    with pytest.raises(Exception):
        check_notfound_task()

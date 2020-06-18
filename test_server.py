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


def test_empty_todo():
    DAO = TodoDAO()
    assert len(DAO.get_all()) == 0


# Test raise exception when task is absent added
def test_notfound_todo():
    DAO = TodoDAO()
    empty = DAO.create({'task': ''})
    if empty is None:
        raise TypeError

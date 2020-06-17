from server import TodoDAO
import pytest
from werkzeug.exceptions import NotFound


def test_list_todo():
    DAO = TodoDAO()
    t1 = DAO.create({'task': 'test-todo'})
    assert t1 is not None
    assert t1['id'] > 0
    t2 = DAO.get(t1['id'])
    assert t2 is not None
    assert t2['task'] == t1['task']
    assert t2['createdAt'] is not None


def test_empty_todo():
    # we test that our Db is not empty
    DAO = TodoDAO()
    assert len(DAO.getAll()) != 0


def test_notfound_todo():
    pass
    DAO = TodoDAO()
    # if todo id is absent api.abort will raise a 404 Not Found HTTP Exception and the test will pass
    with pytest.raises(NotFound):
        assert DAO.get(99)

import pytest
import os
from utility.db import DB

@pytest.fixture
def test_db():
    # Setup test database
    test_tables = {
        'users': {'id': 0, 'name': '', 'age': 0},
        'posts': {'id': 0, 'title': '', 'content': ''}
    }
    db = DB(tables=test_tables, name='test_database')
    yield db
    # Cleanup after tests
    if os.path.exists(db.path):
        os.remove(db.path)

def test_db_initialization(test_db):
    assert os.path.exists(test_db.path)
    assert 'users' in test_db.db.table_names()
    assert 'posts' in test_db.db.table_names()

def test_insert_and_retrieve_data(test_db):
    # Test single dict insert
    user_data = {'id': 1, 'name': 'John Doe', 'age': 30}
    test_db.do('users', user_data)
    
    # Test retrieval
    users = test_db.do('users')
    assert len(users) == 1
    assert users[0]['name'] == 'John Doe'

def test_batch_insert(test_db):
    # Test list insert
    users = [
        {'id': 1, 'name': 'John', 'age': 30},
        {'id': 2, 'name': 'Jane', 'age': 25}
    ]
    test_db.do('users', users)
    
    result = test_db.do('users')
    assert len(result) == 2

def test_conditional_query(test_db):
    users = [
        {'id': 1, 'name': 'John', 'age': 30},
        {'id': 2, 'name': 'Jane', 'age': 25}
    ]
    test_db.do('users', users)
    
    result = test_db.do('users', condition="age = 30")
    assert len(result) == 1
    assert result[0]['name'] == 'John'

def test_update_data(test_db):
    # Insert initial data
    test_db.do('users', {'id': 1, 'name': 'John', 'age': 30})
    
    # Update data
    update_data = {'name': 'John Updated', 'age': 31}
    test_db.do('users', update_data, condition="id = 1")
    
    result = test_db.do('users', condition="id = 1")
    assert result[0]['name'] == 'John Updated'
    assert result[0]['age'] == 31

def test_delete_data(test_db):
    # Insert test data
    test_db.do('users', {'id': 1, 'name': 'John', 'age': 30})
    
    # Test conditional delete
    test_db.do('users', condition="id = 1", delete=True)
    result = test_db.do('users')
    assert len(result) == 0
    
    # Test clear table
    test_db.do('users', {'id': 1, 'name': 'John', 'age': 30})
    test_db.do('users', delete=True)
    result = test_db.do('users')
    assert len(result) == 0

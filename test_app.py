import os, tempfile
from app import create_app

def test_home():
    app=create_app(); app.config.update(TESTING=True,SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
    with app.test_client() as c: assert c.get('/').status_code==200

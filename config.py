import os
basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/test_db' #+ os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

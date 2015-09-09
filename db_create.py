"""
Создает таблицы в БД
"""
from runserver import db
from models import UserRequests
db.create_all()

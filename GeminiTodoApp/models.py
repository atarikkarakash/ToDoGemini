from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


# Bir classımız olacak  ve bu class'ı database'deki değşkenimiz olan base'i ekiyoruz.
# Çünkü bu sınıf database'de kolonalrımı oluşturmamdan sorumlu olacak

class Todo(Base):
    __tablename__ = 'todos'  # __tablename__ sabit değişkendir direkt böyle yazmamız gerekioyr. Ardından ismini verebiliriz tablonun

    id = Column(Integer, primary_key=True, index=True) # Primary key her bir satırın farklı bir id olduğunu söyler.
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)
    role = Column(String)
    phone_number = Column(String)

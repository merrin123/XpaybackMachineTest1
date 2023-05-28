from sqlalchemy import Column, String, Integer
from .postgresdatabase import PostgresBase

class PostgresUser(PostgresBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
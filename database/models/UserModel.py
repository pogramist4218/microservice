from sqlalchemy import Column, Integer, String, Date
from database.connector import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    sex = Column(String(1))
    birth_date = Column(Date())

from sqlalchemy import Column, Integer, String, Float
from database.connector import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer(), primary_key=True)
    name = Column(String(500))
    price = Column(Float())

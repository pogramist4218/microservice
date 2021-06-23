from sqlalchemy import Column, Integer, String, Float
from database.connector import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer(), primary_key=True) #todo скобки у Интежер не надо
    name = Column(String(500))
    price = Column(Float())#todo лучше децимал + в постгресс есть тип money

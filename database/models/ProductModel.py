from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import validates
from database.connector import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    price = Column(MONEY)

    @validates("name")
    def validate_name(self, key: int, item: str) -> str:
        if not item:
            raise AttributeError("name has been null")
        elif item.isnumeric():
            raise TypeError("name has been numeric")
        return item

    @validates("price")
    def validate_price(self, key: int, item: str) -> str:
        if not item:
            raise AttributeError("price has been null")
        return item

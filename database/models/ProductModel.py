from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import MONEY

from database.connector import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    price = Column(MONEY)

    @validates("name")
    def validate_name(self, key: int, item: str) -> str:
        item = item.strip()
        if not item:
            raise AttributeError(f"{key} has been null")
        elif item.isnumeric():
            raise TypeError(f"{key} has been numeric")
        return item

    @validates("price")
    def validate_price(self, key: int, item: str) -> str:
        item = item.strip()
        if not item:
            raise AttributeError(f"{key} has been null")
        return item

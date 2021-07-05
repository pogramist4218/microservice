from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, Date, ForeignKey

from database.connector import Base
from database.models.UserModel import UserModel
from database.models.ProductModel import ProductModel


class PurchaseModel(Base):
    __tablename__ = "purchase"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey(
        column=UserModel.id,
        onupdate="CASCADE",
        ondelete="CASCADE",
    ))
    product_id = Column(Integer(), ForeignKey(
        column=ProductModel.id,
        onupdate="CASCADE",
        ondelete="CASCADE",
    ))
    purchase_date = Column(Date())

    @validates("user_id", "product_id")
    def validate_user_id_or_product_id(self, key: int, item: int) -> int:
        return item

    @validates("purchase_date")
    def validate_purchase_date(self, key: int, item: datetime) -> datetime:
        if not item:
            raise AttributeError(f"{key} has been null")
        try:
            datetime.strptime(item, '%d.%m.%Y')
        except ValueError:
            raise TypeError(f"{key} has not been like <DD.MM.YYYY>")
        return item

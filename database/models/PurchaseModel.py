from datetime import datetime

from sqlalchemy import Column, Integer, Date, ForeignKey
from database.connector import Base
from sqlalchemy.orm import validates
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

    @validates("user_id")
    def validate_user_id(self, key: int, item: int) -> int:#todo зачем передавать key если ты его не юзаешь
        if not item:
            raise AttributeError("user_id has been null")
        return item

    @validates("product_id")
    def validate_product_id(self, key: int, item: int) -> int:#todo зачем передавать key если ты его не юзаешь
        if not item:
            raise AttributeError("product_id has been null")
        return item

    @validates("purchase_date")
    def validate_purchase_date(self, key: int, item: datetime) -> datetime:#todo зачем передавать key если ты его не юзаешь
        if not item:
            raise AttributeError("purchase_date has been null")
        try:
            datetime.strptime(item, '%d.%m.%Y')
        except ValueError:
            raise TypeError("purchase_date has not been like <DD.MM.YYYY>")
        return item

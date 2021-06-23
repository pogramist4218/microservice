from sqlalchemy import Column, Integer, Date, ForeignKey
from database.connector import Base


class PurchaseModel(Base):
    __tablename__ = "purchase"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey(
        column="users.id",
        onupdate="CASCADE",
        ondelete="CASCADE",
    ))
    product_id = Column(Integer(), ForeignKey(
        column="products.id", #todo если мы переименуем поле в табличке :), лучше модель указывать
        onupdate="CASCADE",
        ondelete="CASCADE",
    ))
    purchase_date = Column(Date())

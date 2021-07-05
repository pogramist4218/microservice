from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, String, Date, SmallInteger

from database.connector import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    sex = Column(SmallInteger)
    birth_date = Column(Date)

    @validates("name", "surname")
    def validate_name_or_surname(self, key: str, item: str) -> str:
        if not item.isalpha():
            raise TypeError(f"{key} has not valid symbols")
        return item

    @validates("sex")
    def validate_sex(self, key: str, item: int) -> int:
        if item not in [0, 1, 2, 9]:
            raise TypeError(f"{key} has not been in allowed types")
        return item

    @validates("birth_date")
    def validate_birth_date(self, key: str, item: datetime) -> datetime:
        if not item:
            raise AttributeError(f"{key} has been null")
        try:
            datetime.strptime(item, '%d.%m.%Y')
        except ValueError:
            raise TypeError(f"{key} has not been like <DD.MM.YYYY>")
        return item

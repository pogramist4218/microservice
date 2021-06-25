from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, SmallInteger
from sqlalchemy.orm import validates
from database.connector import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    sex = Column(SmallInteger)
    birth_date = Column(Date)

    @validates("name")
    def validate_name(self, key: str, item: str) -> str:
        if not item:
            raise AttributeError("name has been null")
        elif item.isnumeric():
            raise TypeError("name has been numeric")
        return item

    @validates("surname")
    def validate_surname(self, key: str, item: str) -> str:
        if not item:
            raise AttributeError("surname has been null")
        elif item.isnumeric():
            raise TypeError("surname has been numeric")
        return item

    @validates("sex")
    def validate_sex(self, key: str, item: int) -> int:
        if not item:
            raise AttributeError("sex has been null")
        elif item not in [0, 1, 2, 9]:
            raise TypeError("sex has not been in allowed types")
        return item

    @validates("birth_date")
    def validate_birth_date(self, key: str, item: datetime) -> datetime:
        if not item:
            raise AttributeError("birth_date has been null")
        try:
            datetime.strptime(item, '%d.%m.%Y')
        except ValueError:
            raise TypeError("birth_date has not been like <DD.MM.YYYY>")
        return item

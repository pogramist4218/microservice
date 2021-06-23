from datetime import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import validates
from database.connector import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    sex = Column(String(1)) #todo почему один символ?
    birth_date = Column(Date())

#todo ждешь стр тип и кроме него ничего не может быть И при этом проверяешь на число
    @validates("name")
    def validate_name(self, key: str, item: str) -> str:
        if not item:
            raise AttributeError("name has been null")
        elif item.isnumeric():
            raise TypeError("name has been numeric")
        return item

# todo ждешь стр тип и кроме него ничего не может быть И при этом проверяешь на число ТОЖЕ ЧТО И ИМЯ выше
    @validates("surname")
    def validate_surname(self, key: str, item: str) -> str:
        if not item:
            raise AttributeError("surname has been null")
        elif item.isnumeric():
            raise TypeError("surname has been numeric")
        return item

    @validates("sex") #todo вообще не то: если маленькие символы или в другой раскладке + почему один символ???
    def validate_sex(self, key: str, item: str) -> str:
        if not item:
            raise AttributeError("sex has been null")
        elif item != "M" or item != "W":
            raise TypeError("sex has not been <M> or <W>")
        return item

    @validates("birth_date")
    def validate_birth_date(self, key: str, item: datetime) -> datetime:
        if not item:
            raise AttributeError("birth_date has been null")
        elif datetime.strptime(item, '%d.%m.%Y'):
            raise TypeError("birth_date has not been like <DD.MM.YYYY>")
        return item

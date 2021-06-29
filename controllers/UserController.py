from datetime import datetime

from logger import logger
from database.connector import session, Query
from database.models.UserModel import UserModel


class UserController:
    # https://ru.wikipedia.org/wiki/ISO_5218
    sex_types = {
        0: "Not known",
        1: "Male",
        2: "Female",
        9: "Not applicable",
    }

    def read_users(self, user_id: int = None) -> dict:
        if user_id:
            prepare_query = Query([UserModel]).filter(UserModel.id == user_id)
        else:
            prepare_query = Query([UserModel])

        try:
            users = prepare_query.with_session(session).all()
        except Exception as e:
            logger.error(e.args)

            return {"message": "Failed reading"}
        else:
            result = [{
                "name": user.name,
                "surname": user.surname,
                "sex": self.sex_types[user.sex],
                "birth_date": user.birth_date.strftime('%d.%m.%Y')
            } for user in users]

            logger.info("Success reading users")

            return {"message": "Success reading", "users": result}

    def create_user(self,
                    name: str = None,
                    surname: str = None,
                    sex: int = None,
                    birth_date: datetime = None) -> dict:
        try:
            user = UserModel(
                name=name,
                surname=surname,
                sex=sex,
                birth_date=birth_date,
            )

            session.add(user)
            session.commit()
        except AttributeError as e:
            session.rollback()

            logger.error(e)
            return {"message": "Failed creating: exist not-null argument"}
        except TypeError as e:
            session.rollback()

            logger.error(e)
            return {"message": "Failed creating: not valid type argument"}
        except Exception as e:
            session.rollback()

            logger.error(e)
            return {"message": "Failed creating"}
        else:
            logger.info(f"Success creating user({user.id})")
            return {"message": "Success creating user", "user id": user.id}

    def update_user(self,
                    user_id: int,
                    name: str = None,
                    surname: str = None,
                    sex: int = None,
                    birth_date: datetime = None) -> dict:
        user = session.query(UserModel).get(user_id)
        if user:

            try:
                if name:
                    user.name = name
                if surname:
                    user.surname = surname
                if sex:
                    user.sex = sex
                if birth_date:
                    user.birth_date = birth_date

                session.commit()
            except AttributeError as e:
                session.rollback()

                logger.error(e)
                return {"message": "Failed creating: exist not-null argument"}
            except TypeError as e:
                session.rollback()

                logger.error(e)
                return {"message": "Failed creating: not valid type argument"}
            except Exception as e:
                session.rollback()
                logger.error(e.args)

                return {"message": "Failed updating"}
            else:
                message = f"Success updating user({user_id})"
                logger.info(message)

                return {"message": message}
        else:
            return {"message": f"Failed updating: not exist user({user_id})"}

    def delete_user(self, user_id: int) -> dict:

        try:
            session.query(UserModel).filter(UserModel.id == user_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e.args)

            return {"message": f"Failed deleting: not exist user({user_id})"}
        else:
            message = f"Success deleting user({user_id})"
            logger.info(message)

            return {"message": message}

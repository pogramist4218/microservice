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

    def read_users(self, user_id: int = None) -> list:
        if user_id:
            prepare_query = Query([UserModel]).filter(UserModel.id == user_id)
        else:
            prepare_query = Query([UserModel])

        try:
            users = prepare_query.with_session(session).all()
            if not users:
                logger.error(f"Failed reading: not exists user({user_id})")

                return [{"message": f"Failed reading: not exists user({user_id})"}, 404]
        except Exception as e:
            logger.error(e.args)

            return [{"message": "Failed reading"}, 400]
        else:
            result = [{
                "name": user.name,
                "surname": user.surname,
                "sex": self.sex_types[user.sex],
                "birth_date": user.birth_date.strftime('%d.%m.%Y')
            } for user in users]

            logger.info("Success reading users")

            return [{"message": "Success reading", "users": result}, 200]

    def create_user(self,
                    name: str = None,
                    surname: str = None,
                    sex: int = None,
                    birth_date: datetime = None) -> list:
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
            return [{"message": "Failed creating: exist null argument"}, 400]
        except TypeError as e:
            session.rollback()

            logger.error(e)
            return [{"message": "Failed creating: not valid type argument"}, 400]
        except Exception as e:
            session.rollback()

            logger.error(e)
            return [{"message": "Failed creating"}, 400]
        else:
            logger.info(f"Success creating user({user.id})")
            return [{"message": "Success creating user", "user id": user.id}, 200]

    def update_user(self,
                    user_id: int,
                    name: str = None,
                    surname: str = None,
                    sex: int = None,
                    birth_date: datetime = None) -> list:
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
                return [{"message": "Failed creating: exist null argument"}, 400]
            except TypeError as e:
                session.rollback()

                logger.error(e)
                return [{"message": "Failed creating: not valid type argument"}, 400]
            except Exception as e:
                session.rollback()
                logger.error(e.args)

                return [{"message": "Failed updating"}, 400]
            else:
                message = f"Success updating user({user_id})"
                logger.info(message)

                return [{"message": message}, 200]
        else:
            return [{"message": f"Failed updating: not exist user({user_id})"}, 404]

    def delete_user(self, user_id: int) -> list:

        try:
            session.query(UserModel).filter(UserModel.id == user_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e.args)

            return [{"message": f"Failed deleting: not exist user({user_id})"}, 404]
        else:
            message = f"Success deleting user({user_id})"
            logger.info(message)

            return [{"message": message}, 200]

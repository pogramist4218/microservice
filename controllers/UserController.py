from database.connector import session, Query
from database.models.UserModel import UserModel
from logger import logger


class UserController:
    def read_users(self, user_id: int = None) -> dict:
        if user_id:
            prepare_query = Query([UserModel]).filter(UserModel.id == user_id)
        else:
            prepare_query = Query([UserModel])

        try:
            users = prepare_query.with_session(session).all()
        except Exception as e:
            logger.error(e.args)

            return {"error": True, "message": "Failed reading"}
        else:
            result = [{
                "name": user.name,
                "surname": user.surname,
                "sex": user.sex,
                "birth_date": user.birth_date.strftime('%d.%m.%Y')
            } for user in users]

            logger.info("Success reading users")

            return {"error": False, "message": "Success reading", "users": result}

    def create_user(self, name: str = None, surname: str = None, sex: str = None, birth_date: str = None) -> dict:
        try:
            user = UserModel(
                name=name,
                surname=surname,
                sex=sex,
                birth_date=birth_date,#todo тут должна быть дата, но в параметрах иождаешь СТР
            )

            session.add(user)
            session.commit()
        except AttributeError as e:
            session.rollback()

            logger.error(e)
            return {"error": True, "message": "Failed creating: exist not-null argument"}
        except TypeError as e:
            session.rollback()

            logger.error(e)
            return {"error": True, "message": "Failed creating: not valid type argument"}
        except Exception as e:
            session.rollback()

            logger.error(e)
            return {"error": True, "message": "Failed creating"}
        else:
            logger.info("Success creating users")
            return {"error": False, "message": "Success creating", "user id": user.id}

from database.connector import session
from database.models.UserModel import UserModel


class UserController:
    def create_user(self, **kwargs):
        user = UserModel(**kwargs)

        session.add(user)
        session.commit()

        if user.id:
            return {"error": False, "message": "Successfully create new user"}
        return {"error": True, "message": "Fail to create new user"}

    def read_users(self, params):
        if 'id' in params.keys():
            users = session.query(UserModel).filter_by(id=params['id']).all()
        else:
            users = session.query(UserModel).all()

        result = [{
            "name": user.name,
            "surname": user.surname,
            "sex": user.sex,
            "birth_date": self._get_birth_date(user.birth_date)
        } for user in users]

        return {"error": False, "message": "success", "user": result}

    def update_user(self, **kwargs):
        session.query(UserModel).filter_by(id=kwargs['user_id']).update(kwargs['new_attrs'])
        session.commit()

        return {"error": False, "message": f"Successfully update user with id={kwargs['user_id']}"}

    def delete_user(self, user_id):
        session.query(UserModel).filter_by(id=user_id).delete()
        session.commit()

        return {"error": False, "message": f"Successfully delete user with id={user_id}"}

    def _get_birth_date(self, date):
        return date.strftime('%d.%m.%Y')

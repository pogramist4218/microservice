from flask import Flask, request


from configs import APP_CONFIG #todo не вижу конфига
from controllers.UserController import UserController

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return {"message": "Hello, world"}


@app.route("/user/create", methods=["POST"])
def handle_create_user():
    controller = UserController()
    response = controller.create_user(**request.get_json())
    return {"response": response}

#todo зачем два роута ?
@app.route("/user/read", methods=["GET"])
@app.route("/user/read/<int:user_id>", methods=["GET"])
def handle_read_user(user_id: int = None) -> dict:
    controller = UserController()
    response = controller.read_users(user_id)
    return {"response": response}

#todo https://ru.stackoverflow.com/questions/1070324/%D0%A0%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0-%D0%BE%D1%82%D0%BB%D0%B8%D1%87%D0%B8%D1%8F-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-put-%D0%B8-patch-%D0%B2-rest
@app.route("/user/update/<int:user_id>", methods=["PATCH"])
def handle_update_user(user_id: int):
    return {"method": "update", "args": user_id}


@app.route("/user/delete/<int:user_id>", methods=["DELETE"])
def handle_delete_user(user_id: int):
    return {"method": "delete", "args": user_id}


if __name__ == "__main__":
    app.run(**APP_CONFIG)

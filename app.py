from flask import Flask, request

from configs import APP_CONFIG
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


@app.route("/user/read", methods=["GET"])
@app.route("/user/read/<int:user_id>", methods=["GET"])
def handle_read_user(user_id: int = None) -> dict:
    controller = UserController()
    response = controller.read_users(user_id)
    return {"response": response}


@app.route("/user/update/<int:user_id>", methods=["PATCH"])
def handle_update_user(user_id: int):
    return {"method": "update", "args": user_id}


@app.route("/user/delete/<int:user_id>", methods=["DELETE"])
def handle_delete_user(user_id: int):
    return {"method": "delete", "args": user_id}


if __name__ == "__main__":
    app.run(**APP_CONFIG)

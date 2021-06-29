from flask import Flask, request

from configs import APP_CONFIG
from controllers.UserController import UserController
from controllers.ProductController import ProductController
from controllers.PurchaseController import PurchaseController

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello() -> dict:
    return {"message": "Hello, world"}


@app.route("/user/create", methods=["POST"])
def handle_create_user() -> dict:
    controller = UserController()
    response = controller.create_user(**request.get_json())
    return {"response": response}


@app.route("/user/read", methods=["GET"])
@app.route("/user/read/<int:user_id>", methods=["GET"])
def handle_read_user(user_id: int = None) -> dict:
    controller = UserController()
    response = controller.read_users(user_id)
    return {"response": response}


@app.route("/user/update/<int:user_id>", methods=["PUT"])
def handle_update_user(user_id: int) -> dict:
    controller = UserController()
    response = controller.update_user(user_id, **request.get_json())
    return {"response": response}


@app.route("/user/delete/<int:user_id>", methods=["DELETE"])
def handle_delete_user(user_id: int) -> dict:
    controller = UserController()
    response = controller.delete_user(user_id)
    return {"response": response}


@app.route("/product/create", methods=["POST"])
def handle_create_product() -> dict:
    controller = ProductController()
    response = controller.create_product(**request.get_json())
    return {"response": response}


@app.route("/product/read", methods=["GET"])
@app.route("/product/read/<int:product_id>", methods=["GET"])
def handle_read_product(product_id: int = None) -> dict:
    controller = ProductController()
    response = controller.read_products(product_id)
    return {"response": response}


@app.route("/product/update/<int:product_id>", methods=["PUT"])
def handle_update_product(product_id: int) -> dict:
    controller = ProductController()
    response = controller.update_product(product_id, **request.get_json())
    return {"response": response}


@app.route("/product/delete/<int:product_id>", methods=["DELETE"])
def handle_delete_product(product_id: int) -> dict:
    controller = ProductController()
    response = controller.delete_product(product_id)
    return {"response": response}


@app.route("/purchase/create", methods=["POST"])
def handle_create_purchase() -> dict:
    controller = PurchaseController()
    response = controller.create_purchase(**request.get_json())
    return {"response": response}


@app.route("/purchase/read", methods=["GET"])
@app.route("/purchase/read/<int:purchase_id>", methods=["GET"])
def handle_read_purchase(purchase_id: int = None) -> dict:
    controller = PurchaseController()
    response = controller.read_purchases(purchase_id)
    return {"response": response}


@app.route("/purchase/update/<int:purchase_id>", methods=["PUT"])
def handle_update_purchase(purchase_id: int) -> dict:
    controller = PurchaseController()
    response = controller.update_purchase(purchase_id, **request.get_json())
    return {"response": response}


@app.route("/purchase/delete/<int:purchase_id>", methods=["DELETE"])
def handle_delete_purchase(purchase_id: int) -> dict:
    controller = PurchaseController()
    response = controller.delete_purchase(purchase_id)
    return {"response": response}


@app.route("/purchase/filter-by-user/<string:field>/<string:value>", methods=["GET"])
def handle_filter_by_user_field(field: str, value: str) -> dict:
    controller = PurchaseController()
    response = controller.filter_by_user_field(field, value)
    return {"response": response}


@app.route("/purchase/user/<int:user_id>", methods=["GET"])
def handle_user_purchases(user_id: int) -> dict:
    controller = PurchaseController()
    response = controller.user_purchases(user_id)
    return {"response": response}


if __name__ == "__main__":
    app.run(**APP_CONFIG)

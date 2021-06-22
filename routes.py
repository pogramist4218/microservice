from flask import request

from app import app
from controllers.UserController import UserController
from controllers.ProductController import ProductController
from controllers.PurchaseController import PurchaseController


@app.route('/')
def hello():
    return {"hello": "world"}


# CRUD for UsersModel
@app.route('/users', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def handle_users():
    controller = UserController()

    # CREATE
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            response = controller.create_user(
                name=data['name'],
                surname=data['surname'],
                sex=data['sex'],
                birth_date=data['birth_date'],
            )
            return response
        else:
            return {"error": True, "message": "Not valid request args"}

    # READ
    elif request.method == 'GET':
        response = controller.read_users(request.args)

        return response

    # UPDATE
    elif request.method == 'PATCH':
        if request.is_json:
            data = request.get_json()
            response = controller.update_user(user_id=data['id'], new_attrs=data['update'])
            return response
        else:
            return {"error": True, "message": "Not valid request args"}

    # DELETE
    elif request.method == 'DELETE':
        if 'id' in request.args:
            response = controller.delete_user(request.args['id'])
            return response
        else:
            return {"error": True, "message": "Not valid request args"}

    else:
        return {"error": True, "message": "Not valid request method"}


# CRUD for ProductModel
@app.route('/products', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def handle_products():
    controller = ProductController()

    # CREATE
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            response = controller.create_product(
                name=data['name'],
                price=data['price'],
            )
            return response
        else:
            return {"error": True, "message": "Not valid request args"}

    # READ
    elif request.method == 'GET':
        response = controller.read_products(request.args)

        return response

    # UPDATE
    elif request.method == 'PATCH':
        if request.is_json:
            data = request.get_json()
            response = controller.update_product(product_id=data['id'], new_attrs=data['update'])
            return response
        else:
            return {"error": True, "message": "Not valid request args"}

    # DELETE
    elif request.method == 'DELETE':
        if 'id' in request.args:
            response = controller.delete_product(request.args['id'])
            return response
        else:
            return {"error": True, "message": "Not valid request args"}

    else:
        return {"error": True, "message": "Not valid request method"}


# CRUD fro PurchaseModel
@app.route('/purchase', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def handle_purchases():
    controller = PurchaseController()

    # CREATE
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            response = controller.create_purchase(
                user_id=data['user_id'],
                product_id=data['product_id'],
                purchase_date=data['purchase_date']
            )
            return response
        else:
            return {"error": True, "message": "Not valid request args"}

    # READ
    elif request.method == "GET":
        response = controller.read_purchases(request.args)

        return response

    # UPDATE
    elif request.method == "PATCH":
        if request.is_json:
            data = request.get_json()
            response = controller.update_purchase(purchase_id=data['id'], new_attrs=data['update'])
            return response
        else:
            return {"error": True, "message": "Not valid request args"}

    # DELETE
    elif request.method == "DELETE":
        if 'id' in request.args:
            response = controller.delete_purchase(request.args['id'])
            return response
        else:
            return {"error": True, "message": "Not valid request args"}

    else:
        return {"error": True, "message": "Not valid request method"}


# Filter purchase by:
#     User:    [name, surname, sex]
#     Product: [name, price]
@app.route('/purchase/filter', methods=['GET'])
def handle_filter_purchases():
    if request.method == "GET":
        if request.is_json:
            controller = PurchaseController()

            data = request.get_json()
            response = controller.filter_purchase(data)

            return response
        return {"error": True, "message": "Not valid request args"}
    return {"error": True, "message": "Not valid request method"}

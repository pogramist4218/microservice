from sqlalchemy.exc import IntegrityError

from database.connector import session
from database.models.PurchaseModel import PurchaseModel
from database.models.UserModel import UserModel
from database.models.ProductModel import ProductModel


class PurchaseController:
    def create_purchase(self, **kwargs):
        purchase = PurchaseModel(**kwargs)

        session.add(purchase)
        try:
            session.commit()
        except IntegrityError:
            return {"error": True, "message": "Fail to create new purchase: check your`s args, "
                                              "maybe this product or user don`t exist?"}

        if purchase.id:
            return {"error": False, "message": "Successfully create new purchase"}
        return {"error": True, "message": "Fail to create new purchase"}

    def read_purchases(self, params: dict) -> str:
        if 'id' in params.keys():
            purchases = session.query(PurchaseModel, UserModel, ProductModel)\
                .filter_by(id=params['id']) \
                .join(UserModel, PurchaseModel.user_id == UserModel.id) \
                .join(ProductModel, PurchaseModel.product_id == ProductModel.id) \
                .all()
        else:
            purchases = session.query(PurchaseModel, UserModel, ProductModel) \
                .join(UserModel, PurchaseModel.user_id == UserModel.id)\
                .join(ProductModel, PurchaseModel.product_id == ProductModel.id)\
                .all()

        result = [{
            "user": {
                "name": purchase['UserModel'].name,
                "surname": purchase['UserModel'].surname,
                "sex": purchase['UserModel'].sex,
                "birth_date": self._get_format_date(purchase['UserModel'].birth_date),
            },
            "product": {
                "name": purchase['ProductModel'].name,
                "price": purchase['ProductModel'].price,
            },
        } for purchase in purchases]

        return {"error": False, "message": "success", "purchases": result}

    def update_purchase(self, **kwargs):
        try:
            session.query(PurchaseModel).filter_by(id=kwargs['purchase_id']).update(kwargs['new_attrs'])
            session.commit()
        except IntegrityError:
            return {"error": True, "message": "Fail to update purchase: check your`s args, "
                                              "maybe this product or user don`t exist?"}

        return {"error": False, "message": f"Successfully update purchase with id={kwargs['purchase_id']}"}

    def delete_purchase(self, purchase_id):
        session.query(PurchaseModel).filter_by(id=purchase_id).delete()
        session.commit()

        return {"error": False, "message": f"Successfully delete purchase with id={purchase_id}"}

    def filter_purchase(self, params):
        prepare_query = session.query(PurchaseModel, UserModel, ProductModel)

        if 'user' in params.keys():
            prepare_query = prepare_query.join(UserModel, PurchaseModel.user_id == UserModel.id).filter_by(**params['user']).all()

        if 'product' in params.keys():
            prepare_query.join(ProductModel, PurchaseModel.product_id == ProductModel.id).filter_by(**params['product'])

        print(prepare_query)

        result = [{
            "user name": item['UserModel'].name,
            "user surname": item['UserModel'].surname,
            "product name": item['ProductModel'].name,
            "product price": item['ProductModel'].price,
            "purchase date": self._get_format_date(item['PurchaseModel'].purchase_date),
        } for item in prepare_query.all()]

        return {"error": False, "message": f"Success", "purchases": result}


    def _get_format_date(self, date):
        return date.strftime('%d.%m.%Y')
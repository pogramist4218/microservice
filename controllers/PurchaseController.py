from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from database.connector import session, Query
from database.models.PurchaseModel import PurchaseModel, UserModel, ProductModel
from logger import logger


class PurchaseController:
    def read_purchases(self, purchase_id: int = None) -> dict:
        prepare_query = Query([PurchaseModel, UserModel, ProductModel]) \
            .join(UserModel, PurchaseModel.user_id == UserModel.id) \
            .join(ProductModel, PurchaseModel.product_id == ProductModel.id)
        if purchase_id:
            prepare_query.filter(PurchaseModel.id == purchase_id)

        try:
            purchases = prepare_query.with_session(session).all()
        except IntegrityError:
            return {"error": True, "message": "Fail to create new purchase: check your`s args, "
                                              "maybe this product or user don`t exist?"}
        except Exception as e:
            logger.error(e.args)

            return {"message": "Failed reading"}
        else:
            result = [{
                "user": {
                    "name": purchase['UserModel'].name,
                    "surname": purchase['UserModel'].surname
                },
                "product": {
                    "name": purchase['ProductModel'].name,
                    "price": purchase['ProductModel'].price,
                },
                "purchase date": purchase['PurchaseModel'].purchase_date.strftime('%d.%m.%Y')
            } for purchase in purchases]

            logger.info("Success reading purchases")

            return {"message": "Success reading", "purchases": result}

    def create_purchase(self,
                        user_id: int = None,
                        product_id: int = None,
                        purchase_date: datetime = None) -> dict:
        try:
            purchase = PurchaseModel(
                user_id=user_id,
                product_id=product_id,
                purchase_date=purchase_date,
            )

            session.add(purchase)
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
            logger.info(f"Success creating purchase({purchase.id})")
            return {"message": "Success creating purchase", "purchase id": purchase.id}

    def update_purchase(self,
                        purchase_id: int,
                        user_id: int = None,
                        product_id: int = None,
                        purchase_date: datetime = None) -> dict:
        purchase = session.query(PurchaseModel).get(purchase_id)
        if purchase:

            try:
                if user_id:
                    purchase.user_id = user_id
                if product_id:
                    purchase.product_id = product_id
                if purchase_date:
                    purchase.purchase_date = purchase_date

                session.add(purchase)
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
                message = f"Success updating purchase({purchase_id})"
                logger.info(message)

                return {"message": message}
        else:
            return {"message": f"Failed updating: not exist purchase({purchase_id})"}

    def delete_purchase(self, purchase_id: int) -> dict:
        try:
            session.query(PurchaseModel).filter(PurchaseModel.id == purchase_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e.args)

            return {"message": f"Failed deleting: not exist purchase({purchase_id})"}
        else:
            message = f"Success deleting purchase({purchase_id})"
            logger.info(message)

            return {"message": message}

    def filter_by_user_field(self, field: str, value: str) -> dict:
        if field in UserModel.__table__.columns:
            prepare_query = Query([UserModel, ProductModel, PurchaseModel])\
                .join(ProductModel) \
                .join(UserModel) \
                .filter_by(**{field: value})

            try:
                purchases = prepare_query.with_session(session).all()
            except Exception as e:
                logger.error(e.args)

                return {"message": "Failed filter"}
            else:
                result = [{
                    "name": product.name,
                    "price": product.price,
                    "date of buying": purchase.purchase_date.strftime('%d.%m.%Y')
                } for user, product, purchase in purchases]

            logger.info(f"Success filter purchases by {field}={value}")

            return {"message": "Success filtering purchases", "purchases": result}
        return {"message": "Failed filter: not have this field"}

    def user_purchases(self, user_id: int) -> dict:
        prepare_query = Query([
            func.count(ProductModel.id),
            func.sum(ProductModel.price),
            ProductModel.name]) \
            .join(PurchaseModel) \
            .filter(PurchaseModel.user_id == user_id) \
            .group_by(ProductModel.name)

        try:
            purchases = prepare_query.with_session(session).all()
        except Exception as e:
            logger.error(e.args)

            return {"message": "Failed filter"}
        else:
            message = f"Success get info about purchases for user({user_id})"

            result = [{
                "name": purchase[2],
                "count": purchase[0],
                "sum": purchase[1]
            } for purchase in purchases]

            logger.info(message)

            return {"message": message, "purchases": result}

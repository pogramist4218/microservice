from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from logger import logger
from database.connector import session, Query
from database.models.PurchaseModel import PurchaseModel, UserModel, ProductModel


class PurchaseController:

    def read_purchases(self, purchase_id: int = None) -> list:
        if purchase_id:
            prepare_query = Query([PurchaseModel, UserModel, ProductModel]) \
                .join(UserModel, PurchaseModel.user_id == UserModel.id) \
                .join(ProductModel, PurchaseModel.product_id == ProductModel.id)\
                .filter(PurchaseModel.id == purchase_id)
        else:
            prepare_query = Query([PurchaseModel, UserModel, ProductModel]) \
                .join(UserModel, PurchaseModel.user_id == UserModel.id) \
                .join(ProductModel, PurchaseModel.product_id == ProductModel.id)

        try:
            purchases = prepare_query.with_session(session).all()
            if not purchases:
                logger.error(f"Failed reading: not exists purchase({purchase_id})")

                return [{"message": f"Failed reading: not exists purchase({purchase_id})"}, 404]
        except IntegrityError:
            return [{"error": True, "message": "Fail to create new purchase: check your`s args, "
                                              "maybe this product or user don`t exist?"}, 404]
        except Exception as e:
            logger.error(e.args)

            return [{"message": "Failed reading"}, 400]
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

            return [{"message": "Success reading", "purchases": result}, 200]

    def create_purchase(self,
                        user_id: int = None,
                        product_id: int = None,
                        purchase_date: datetime = None) -> list:
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
            logger.info(f"Success creating purchase({purchase.id})")
            return [{"message": "Success creating purchase", "purchase id": purchase.id}, 200]

    def update_purchase(self,
                        purchase_id: int,
                        user_id: int = None,
                        product_id: int = None,
                        purchase_date: datetime = None) -> list:
        purchase = session.query(PurchaseModel).get(purchase_id)
        if purchase:

            try:
                if user_id:
                    purchase.user_id = user_id
                if product_id:
                    purchase.product_id = product_id
                if purchase_date:
                    purchase.purchase_date = purchase_date

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
                message = f"Success updating purchase({purchase_id})"
                logger.info(message)

                return [{"message": message}, 200]
        else:
            return [{"message": f"Failed updating: not exist purchase({purchase_id})"}, 404]

    def delete_purchase(self, purchase_id: int) -> list:
        purchase = session.query(PurchaseModel).get(purchase_id)
        if purchase:

            try:
                session.query(PurchaseModel).filter(PurchaseModel.id == purchase_id).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(e.args)

                return [{"message": f"Failed deleting: not exist purchase({purchase_id})"}, 404]
            else:
                message = f"Success deleting purchase({purchase_id})"
                logger.info(message)

                return [{"message": message}, 200]
        else:
            return [{"message": f"Failed deleting: not exist purchase({purchase_id})"}, 404]

    def filter_by_user_field(self, field: str, value: str) -> list:
        prepare_query = Query([UserModel, ProductModel, PurchaseModel])\
            .join(ProductModel) \
            .join(UserModel) \
            .filter_by(**{field: value})

        try:
            purchases = prepare_query.with_session(session).all()
            if not purchases:
                logger.error(f"Failed reading: not exists purchases by {field}={value}")

                return [{"message": f"Failed reading: not exists purchases by {field}={value}"}, 404]
        except Exception as e:
            logger.error(e.args)

            return [{"message": "Failed filter"}, 400]
        else:
            result = [{
                "name": product.name,
                "price": product.price,
                "date of buying": purchase.purchase_date.strftime('%d.%m.%Y')
            } for user, product, purchase in purchases]

        logger.info(f"Success filter purchases by {field}={value}")

        return [{"message": "Success filtering purchases", "purchases": result}, 200]

    def user_purchases(self, user_id: int) -> list:
        prepare_query = Query([
            func.count(ProductModel.id),
            func.sum(ProductModel.price),
            ProductModel.name]) \
            .join(PurchaseModel) \
            .filter(PurchaseModel.user_id == user_id) \
            .group_by(ProductModel.name)

        try:
            purchases = prepare_query.with_session(session).all()
            if not purchases:
                logger.error(f"Failed reading: not exists purchases")

                return [{"message": f"Failed reading: not exists purchases"}, 404]
        except Exception as e:
            logger.error(e.args)

            return [{"message": "Failed filter"}, 400]
        else:
            message = f"Success get info about purchases for user({user_id})"

            result = [{
                "name": purchase[2],
                "count": purchase[0],
                "sum": purchase[1]
            } for purchase in purchases]

            logger.info(message)

            return [{"message": message, "purchases": result}, 200]

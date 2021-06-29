from logger import logger
from database.connector import session, Query
from database.models.ProductModel import ProductModel


class ProductController:

    def read_products(self, product_id: int = None) -> dict:
        if product_id:
            prepare_query = Query([ProductModel]).filter(ProductModel.id == product_id)
        else:
            prepare_query = Query([ProductModel])

        try:
            products = prepare_query.with_session(session).all()
        except Exception as e:
            logger.error(e.args)

            return {"message": "Failed reading"}
        else:
            result = [{
                "name": product.name,
                "price": product.price,
            } for product in products]

            logger.info("Success reading products")

            return {"message": "Success reading", "products": result}

    def create_product(self,
                       name: str = None,
                       price: float = None) -> dict:
        try:
            product = ProductModel(
                name=name,
                price=price,
            )

            session.add(product)
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
            logger.info(f"Success creating product({product.id})")
            return {"message": "Success creating product", "product id": product.id}

    def update_product(self,
                       product_id: int,
                       name: str = None,
                       price: float = None) -> dict:
        product = session.query(ProductModel).get(product_id)
        if product:

            try:
                if name:
                    product.name = name
                if price:
                    product.price = price

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
                message = f"Success updating product({product_id})"
                logger.info(message)

                return {"message": message}
        else:
            return {"message": f"Failed updating: not exist product({product_id})"}

    def delete_product(self, product_id: int) -> dict:
        try:
            session.query(ProductModel).filter(ProductModel.id == product_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e.args)

            return {"message": f"Failed deleting: not exist product({product_id})"}
        else:
            message = f"Success deleting product({product_id})"
            logger.info(message)

            return {"message": message}

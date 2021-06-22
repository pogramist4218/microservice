from database.connector import session
from database.models.ProductModel import ProductModel


class ProductController:
    def create_product(self, **kwargs):
        product = ProductModel(**kwargs)

        session.add(product)
        session.commit()

        if product.id:
            return {"error": False, "message": "Successfully create new product"}
        return {"error": True, "message": "Fail to create new product"}

    def read_products(self, params):
        if 'id' in params.keys():
            products = session.query(ProductModel).filter_by(id=params['id']).all()
        else:
            products = session.query(ProductModel).all()

        result = [{
            "name": product.name,
            "price": product.price,
        } for product in products]

        return {"error": False, "message": "success", "product": result}

    def update_product(self, **kwargs):
        session.query(ProductModel).filter_by(id=kwargs['product_id']).update(kwargs['new_attrs'])
        session.commit()

        return {"error": False, "message": f"Successfully update product with id={kwargs['product_id']}"}

    def delete_product(self, product_id):
        session.query(ProductModel).filter_by(id=product_id).delete()
        session.commit()

        return {"error": False, "message": f"Successfully delete product with id={product_id}"}

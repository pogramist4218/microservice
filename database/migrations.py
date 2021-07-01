import os
import sys

sys.path.append(os.getcwd())

import random
from faker import Faker
from faker_vehicle import VehicleProvider
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy import create_engine, \
    MetaData, \
    Table, \
    Column, \
    Integer, \
    SmallInteger, \
    String, \
    Date, \
    ForeignKey

from configs import DB_CONFIG

engine = create_engine(DB_CONFIG)
metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(255), nullable=False),
              Column('surname', String(255), nullable=False),
              Column('sex', SmallInteger, nullable=False),
              Column('birth_date', Date, nullable=False),
              )

products = Table('products', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String(255), nullable=False),
                 Column('price', MONEY, nullable=False),
                 )

purchases = Table('purchase', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('user_id', Integer, ForeignKey(
                      column="users.id",
                      onupdate="CASCADE",
                      ondelete="CASCADE",
                  )),
                  Column('product_id', Integer, ForeignKey(
                      column="products.id",
                      onupdate="CASCADE",
                      ondelete="CASCADE",
                  )),
                  Column('purchase_date', Date, nullable=False),
                  )

metadata.create_all(engine)

fake = Faker()
fake.add_provider(VehicleProvider)

mock_users = users.insert().values([
    {
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "sex": random.choice([0, 1, 2, 9]),
        "birth_date": fake.date()
    }
    for _ in range(15)
])
mock_products = products.insert().values([
    {
        "name": fake.machine_make_model(),
        "price": str(random.randint(100, 1000))
    }
    for _ in range(15)
])

engine.execute(mock_users)
engine.execute(mock_products)

result_users = engine.execute(users.select())
result_products = engine.execute(products.select())

users_id = [user[0] for user in result_users]
products_id = [product[0] for product in result_products]
mock_purchases = purchases.insert().values([
    {
        "user_id": random.choice(users_id),
        "product_id": random.choice(products_id),
        "purchase_date": fake.date(),
    }
    for _ in range(50)
])

engine.execute(mock_purchases)

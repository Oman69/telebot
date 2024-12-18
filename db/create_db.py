import uuid

from sqlalchemy import create_engine, func, insert, Boolean
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, UUID, ForeignKey, Float
engine = create_engine('sqlite:///telebot_db.db')


metadata = MetaData()

orders = Table(
    'orders', metadata,
    Column('uid', UUID, primary_key=True),
    Column('number', Integer, autoincrement=True, nullable=False),
    Column('user_id', String, nullable=False),
    Column('datetime_create', DateTime(timezone=True, ), onupdate=func.now()),
    Column('datetime_get', DateTime(timezone=True,)),
    Column('ordered', Boolean, default=False),
)

category = Table(
    'category', metadata,
    Column('uid', UUID, primary_key=True),
    Column('name', String, nullable=False),
)


products = Table(
    'products', metadata,
    Column('uid', UUID, primary_key=True, default=uuid.uuid4()),
    Column('name', String, nullable=False),
    Column('description', String),
    Column('weigh', Integer),
    Column('price', Float, nullable=False),
    Column('category', ForeignKey('category.uid'), nullable=False)
)


orders_products = Table(
    'order_products', metadata,
    Column('uid', UUID, primary_key=True),
    Column('order_id', ForeignKey('orders.uid'), nullable=False),
    Column('product_id', ForeignKey('products.uid'), nullable=False),
    Column('value', Integer, nullable=False),
)


metadata.create_all(engine)

# insert_to_db(products, {'name': 'Салат мимоза', 'weigh': 250, 'price': 200.00})
# insert_to_table(products, {'name': 'Салат крабовый', 'weigh': 220, 'price': 150.00})
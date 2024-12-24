import uuid

from sqlalchemy import func, create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, UUID, ForeignKey, Float, Boolean

engine = create_engine('sqlite:///telebot_db.db')

metadata = MetaData()

orders = Table(
    'orders', metadata,
    Column('uid', UUID, primary_key=True),
    Column('number', Integer, autoincrement=True, nullable=False, default=1),
    Column('user_id', String, nullable=False),
    Column('datetime_create', DateTime(timezone=True, ), onupdate=func.now()),
    Column('datetime_get', DateTime(timezone=True,)),
    Column('ordered', Boolean, default=False),
)


products = Table(
    'products', metadata,
    Column('uid', UUID, primary_key=True, default=uuid.uuid4()),
    Column('name', String, nullable=False),
    Column('description', String),
    Column('weigh', Integer),
    Column('price', Float, nullable=False),
    Column('category', String, nullable=False)
)

orders_products = Table(
    'orders_products', metadata,
    Column('uid', UUID, primary_key=True),
    Column('order_id', ForeignKey('orders.uid'), nullable=False),
    Column('product_id', ForeignKey('products.uid'), nullable=False),
    Column('value', Integer, nullable=False, default=1),
)


metadata.create_all(engine)
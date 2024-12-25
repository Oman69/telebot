import datetime
import uuid

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, UUID, ForeignKey, Float, Boolean

engine = create_engine('sqlite:///telebot_db.db')

metadata = MetaData()

orders = Table(
    'orders', metadata,
    Column('uid', UUID, primary_key=True, unique=False),
    Column('number', Integer, autoincrement=True, default=0),
    Column('user_id', String, nullable=False),
    Column('datetime_create', DateTime, default=datetime.datetime.now()),
    Column('datetime_get', String),
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
    Column('order_id', ForeignKey('orders.uid', ondelete="CASCADE"), nullable=False),
    Column('product_id', ForeignKey('products.uid', ondelete="CASCADE"), nullable=False),
    Column('value', Integer, nullable=False, default=1),
)


metadata.create_all(engine)
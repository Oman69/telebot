import uuid

from sqlalchemy import func
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, UUID, ForeignKey, Float, Boolean

from db.db_utils import insert_to_table, engine

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
    Column('value', Integer, nullable=False),
)


metadata.create_all(engine)


# insert_to_table(products, {'uid': uuid.uuid4(), 'name': 'Салат мимоза', 'weigh': 250, 'price': 200.00, 'category': 'salad'})
# insert_to_table(products, {'uid': uuid.uuid4(),'name': 'Салат крабовый', 'weigh': 220, 'price': 150.00, 'category': 'salad'})
from sqlalchemy import select, update, delete
import uuid
from create_db import products, orders, orders_products, engine
from db_utils import insert_to_table


class Product:

    def __init__(self):
        self.product_data = {'uid':uuid.uuid4()}

    def add_product_to_menu(self):
        insert_to_table(products, params=self.product_data)
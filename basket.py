from sqlalchemy import select, update
import uuid
from create_db import products, orders, orders_products, engine
from db_utils import insert_to_table


class Basket:

    def __init__(self):
        self.order_id = uuid.uuid4()

    def check_product_in_order(self, product_id: uuid.UUID):
        """

        :param product_id:
        :return:
        """
        query = select(orders_products).where(orders_products.c.order_id == self.order_id).where(
            orders_products.c.product_id == product_id)
        k = 0
        value = 0
        with engine.connect() as conn:
            for row in conn.execute(query):
                value = row.t[3]
                k += 1
        return k, value

    def insert_product_to_table(self, user_id: int, product_id: uuid.UUID):
        """

        :param user_id:
        :param product_id:
        :return:
        """
        if self.check_order_in_basket():
            # Добавить заказ в таблицу
            insert_to_table(orders, {'uid': self.order_id, 'user_id': user_id})
        # Добавить заказ-блюдо в таблицу
        insert_to_table(orders_products, {'uid': uuid.uuid4(), 'order_id': self.order_id, 'product_id': product_id})

    def change_value_in_basket(self, product_id: uuid.UUID, current_value: int, operation: bool = True):
        """
        Увеличиваем количество товаров в корзине
        :param product_id:
        :param current_value:
        :param operation:
        :return:
        """
        if operation:
            new_value = current_value + 1
        else:
            new_value = current_value - 1
        # Обновить значение в БД
        update_query = update(orders_products).where(orders_products.c.order_id == self.order_id).where(
            orders_products.c.product_id == product_id).values(value=new_value)
        with engine.connect() as connection:
            connection.execute(update_query)
            connection.commit()

    def get_current_value_by_product_id(self, product_id):
        query = select(orders_products).where(orders_products.c.order_id == self.order_id).where(
            orders_products.c.product_id == product_id)
        with engine.connect() as conn:
            for row in conn.execute(query):
                value = row.t[3]
        return value

    def check_order_in_basket(self):
        """
        Проверить наличие заказа в корзине
        """
        query = select(orders).where(orders.c.uid == self.order_id)
        with engine.connect() as conn:
            for _ in conn.execute(query):
                return True
        return False

    def view_all_basket(self):
        return 'Товары в корзине'

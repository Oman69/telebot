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
        Увеличиваем количество товара в корзине
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
        """
        Получить количество товара корзине
        :param product_id:
        :return:
        """
        value = 0
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

    def get_products_in_basket(self):
        # Получил продукты в корзине
        query = select(orders_products).where(orders_products.c.order_id == self.order_id)
        products_in_basket = []
        with engine.connect() as conn:
            for row in conn.execute(query):
                products_in_basket.append({'product_id': row.t[2], 'value': row.t[3]})
        return products_in_basket

    def view_all_basket(self):
        # Получил продукты в корзине
        products_in_basket = self.get_products_in_basket()

        total = 0
        if bool(products_in_basket):
            message = 'Товары в корзине:\n'
            for item in products_in_basket:
                # if item['value'] > 0: Fix bag
                query = select(products.c.name, products.c.price).where(products.c.uid == item['product_id'])
                with engine.connect() as conn:
                    for row in conn.execute(query):
                        name = row.t[0]
                        price = row.t[1]
                        message += name + ' ' + str(price) + ' руб.' + ' - ' + str(item['value']) + ' шт.\n'
                        total += item['value'] * price

            message += '<b>Сумма заказа: ' + str(total) + ' руб.</b>'

        else:
            message = 'Товары в корзину не добавлены\n'
        return message

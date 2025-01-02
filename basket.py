from sqlalchemy import select, update, delete
import uuid
from create_db import products, orders, orders_products, engine
from db_utils import insert_to_table


class Basket:

    def __init__(self):
        self.order_id = uuid.uuid4()

    def check_product_in_order(self, product_id: uuid.UUID):
        """
        Проверииь наличие продукта в заказе
        :param product_id: Id продукта
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

    def get_last_order_number(self):
        """

        """
        query = select(orders.c.number).order_by(orders.c.number.desc()).limit(1)
        with engine.connect() as conn:
            for row in conn.execute(query):
                return row.t[0]
        return 0

    def insert_product_to_table(self, user_id: int, product_id: uuid.UUID):
        """

        :param user_id:
        :param product_id:
        :return:
        """
        if not self.check_order_in_basket():
            # Получить номер последнего заказа
            new_number = self.get_last_order_number() + 1
            # Добавить заказ в таблицу
            insert_to_table(orders, {'uid': self.order_id, 'user_id': user_id, 'number': new_number})
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
        empty_bs_mess = 'Товары в корзину не добавлены\n'
        # Получил продукты в корзине
        products_in_basket = self.get_products_in_basket()

        total = 0
        if bool(products_in_basket):
            message = 'Товары в корзине:\n'
            for item in products_in_basket:
                if item['value'] > 0:
                    query = select(products.c.name, products.c.price).where(products.c.uid == item['product_id'])
                    with engine.connect() as conn:
                        for row in conn.execute(query):
                            name = row.t[0]
                            price = row.t[1]
                            message += name + ' ' + str(price) + ' руб.' + ' - ' + str(item['value']) + ' шт.\n'
                            total += item['value'] * price

            message += '<b>Сумма заказа: ' + str(total) + ' руб.</b>'
            if total == 0:
                return empty_bs_mess
        else:
            return empty_bs_mess
        return message

    def delete_order(self):
        """
        Удалить заказ из БД
        """

        delete_order_query = delete(orders).where(orders.c.uid == self.order_id)
        with engine.connect() as connection:
            connection.execute(delete_order_query)
            connection.commit()

        delete_products_query = delete(orders_products).where(orders_products.c.order_id == self.order_id)
        with engine.connect() as connection:
            connection.execute(delete_products_query)
            connection.commit()

    def confirm_order(self):
        """
        Подтвердить заказ в БД
        :return:
        """
        update_query = update(orders).where(orders_products.c.order_id == self.order_id).values(ordered=True)
        with engine.connect() as connection:
            connection.execute(update_query)
            connection.commit()

    def save_ordered_time(self, ordered_time):
        """
        Подтвердить заказ в БД
        :return:
        """
        update_query = update(orders).where(orders.c.uid == self.order_id).values(
            datetime_get=ordered_time)
        with engine.connect() as connection:
            connection.execute(update_query)
            connection.commit()

    def get_order_number(self):
        # Получил номер заказа
        query = select(orders.c.number).where(orders.c.uid == self.order_id)
        with engine.connect() as conn:
            for row in conn.execute(query):
                return row.t[0]

    def create_message_about_new_order(self, order_number, receipt_time):
        message = self.view_all_basket().replace('Товары в корзине:',
                                                 '❗ <b>Получен новый заказ c номером - ' + str(order_number) + '</b>')
        message += '\n<b>Время готовности: ' + receipt_time.strftime('%H:%M') + '</b>'
        return message

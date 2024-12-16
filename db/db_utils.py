from sqlalchemy import insert, Table
from db.create_db import engine, products

# insert_query = insert(products).values(name='Салат мимоза', weigh=250, price=200.00)


def insert_to_db(table: Table, params):

    insert_query = insert(table).values(**params)
    try:
        with engine.connect() as connection:
            connection.execute(insert_query)
            connection.commit()
    except Exception as E:
        print(f'Ошибка добавления данных в базу данных: {E}')


# insert_to_db(products, {'name': 'Салат мимоза', 'weigh': 250, 'price': 200.00})
insert_to_db(products, {'name': 'Салат крабовый', 'weigh': 220, 'price': 150.00})
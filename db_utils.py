
from sqlalchemy import insert, Table, select
from create_db import engine


def insert_to_table(table: Table, params):

    insert_query = insert(table).values(**params)
    try:
        with engine.connect() as connection:
            connection.execute(insert_query)
            connection.commit()
    except Exception as E:
        print(f'Ошибка добавления данных в БД: {E}')


def select_from_table(table: Table, column=None, params=None):

    if not params and not column:
        select_query = select(table)
    else:
        select_query = select(table).where(table.c.category == params['value'])
    try:
        with engine.connect() as connection:
            result = connection.execute(select_query)
            return result
    except Exception as E:
        print(f'Ошибка чтения данных из БД: {E}')


# insert_to_table(products, {'uid': uuid.uuid4(), 'name': 'Салат мимоза', 'weigh': 250, 'price': 200.00, 'category': 'salad'})
# insert_to_table(products, {'uid': uuid.uuid4(),'name': 'Салат крабовый', 'weigh': 220, 'price': 150.00, 'category': 'salad'})

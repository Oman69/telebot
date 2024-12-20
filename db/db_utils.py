from sqlalchemy import insert, Table, select, create_engine
engine = create_engine('sqlite:///telebot_db.db')


def insert_to_table(table: Table, params):

    insert_query = insert(table).values(**params)
    try:
        with engine.connect() as connection:
            connection.execute(insert_query)
            connection.commit()
    except Exception as E:
        print(f'Ошибка добавления данных в БД: {E}')


def select_from_table(table: Table, params=None):

    if not params:
        select_query = select(table)
    else:
        select_query = select(table).where(table.c.category == params['value'])
    try:
        with engine.connect() as connection:
            result = connection.execute(select_query)
            return result
    except Exception as E:
        print(f'Ошибка чтения данных из БД: {E}')

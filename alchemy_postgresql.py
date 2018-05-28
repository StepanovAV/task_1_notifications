import os
import sqlalchemy
from sqlalchemy import Column, Integer, String, Table, select


def connect():
    ''' Returns
        connection and a metadata object
    '''
    url = 'postgresql://{}:{}@{}:{}/{}'
    db_user_name = os.environ['POSTGRES_USER']
    db_user_password = os.environ['POSTGRES_PASSWORD']
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_name = os.environ['POSTGRES_DB']
    url = url.format(db_user_name, db_user_password, db_host, db_port, db_name)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    return con, meta


def select_db_table():
    ''' Selects and returns
        table: "messages", which stores all messages.
        Or creates a new table if not exists, and return its self
    '''
    table = Table(
        'messages',
        meta,
        Column('ID', Integer, primary_key=True),
        Column('text', String),
        Column('count', Integer),
        extend_existing=True,
        )
    meta.create_all(con)
    return table


def message_to_db(message, count):
    ''' Inserts
        message and number of its unique words
        into table: "messages"
    '''
    message = table.insert().values(text=message.strip(), count=count)
    con.execute(message)


def messages_from_db():
    ''' Selects and return
        list of all messages and its unique count
        from table: "messages"
    '''
    s = select([table.c.text, table.c.count]).order_by(table.c.count)
    response = con.execute(s)
    return list(response)


con, meta = connect()
table = select_db_table()

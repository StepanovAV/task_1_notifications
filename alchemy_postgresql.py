import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, select, desc, cast


def connect():
    ''' Returns
        connection and a metadata object
    '''
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format('artem', '1111', 'localhost', 5432, 'notifications')
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    return con, meta


def selectDbTable():
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


def messageToDb(table, message, count):
    ''' Inserts
        message and number of its unique words
        into table: "messages"
    '''
    message = table.insert().values(text=message.strip(), count=int(count))
    con.execute(message)


def messagesFromDb(table):
    ''' Selects and return
        list of all messages and its unique count
        from table: "messages"
    '''
    s = select([table.c.text, table.c.count]).order_by(table.c.count)
    response = con.execute(s)
    return list(response)


def delMessages(table):
    ''' Deletes
        all data
        from table: "messages"
    '''
    con.execute(table.delete())

con, meta = connect()

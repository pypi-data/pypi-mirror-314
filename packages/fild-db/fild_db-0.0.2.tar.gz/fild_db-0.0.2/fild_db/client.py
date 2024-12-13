from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


PLAY_EVOLUTIONS = 'play_evolutions'
FKEY_CHECK_OFF = 'SET FOREIGN_KEY_CHECKS=0;'
FKEY_CHECK_ON = 'SET FOREIGN_KEY_CHECKS=1;'
SYNC_COMMIT_OFF = 'SET SYNCHRONOUS_COMMIT TO OFF;'
TRUNC_ALL_TABLES = (
    "SELECT Concat('TRUNCATE TABLE ', table_schema, '.', TABLE_NAME, ';') "
    "FROM INFORMATION_SCHEMA.TABLES "
    "WHERE table_schema in ('{0}') "
    "AND table_name NOT in ({1});"
)


class ConnectionClient:
    connection = None

    def execute(self, sql_script, *args):

        if args:
            result = self.connection.execute(sql_script, args)
        else:
            result = self.connection.execute(text(sql_script))

        if result.returns_rows:
            return result.fetchall()

        return None


class PostgresqlDBClient(ConnectionClient):
    def __init__(self, host='0.0.0.0', port=5432, user='user', password=None,
                 db='db', sync_commit=False, **kwargs):
        self.connection_url = (
            f'postgresql://{user}:{password}@{host}:{port}/{db}'
        )
        self.connection = None
        self._kwargs = kwargs
        self._sync_commit = sync_commit

    def connect(self):
        if self.connection is None:
            engine = create_engine(
                self.connection_url, encoding='utf-8', **self._kwargs
            )
            session = sessionmaker(bind=engine)
            self.connection = session()

            if not self._sync_commit:
                self.connection.execute(SYNC_COMMIT_OFF)
                self.connection.commit()
                self.connection.close()

        return self


class MysqlDBClient(ConnectionClient):
    def __init__(self, host='127.0.0.1', port=3306, user='root',
                 password='mypass', db_name='testengine'):
        self._db = db_name
        self.connection_url = (
            f'mysql://{user}:{password}@{host}:{port}/'
            f'{db_name}?charset=utf8mb4'
        )
        self.connection = None

    def connect(self):
        if self.connection is None:
            engine = create_engine(self.connection_url)
            session = sessionmaker(bind=engine)
            self.connection = session()

        return self

    def trunc_all_tables(self, exclude_tables=None):
        # Test shouldn't truncate internal evolutions table
        exclude_tables = exclude_tables or []
        exclude_tables.append(PLAY_EVOLUTIONS)
        exclude_str = "', '".join(exclude_tables)
        exclude_tables = f"'{exclude_str}'"

        sql = TRUNC_ALL_TABLES.format(self._db, exclude_tables)
        trunc_stmts = ''

        for result in self.connection.execute(sql):
            trunc_stmts += result[0]

        sql = ''.join([FKEY_CHECK_OFF, trunc_stmts, FKEY_CHECK_ON])
        self.execute(sql)


class SqliteDBClient:
    def __init__(self, file_path):
        self._db_file_path = file_path
        self.connection = None

    def connect(self):
        import sqlite3  # pylint: disable=import-outside-toplevel

        if self.connection is None:
            self.connection = sqlite3.connect(self._db_file_path)

        return self

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def read_data(self, sql_script, *args):
        return self.connection.execute(sql_script, args).fetchall()

    def write_data(self, sql_script, *args):
        self.connection.execute(sql_script, args)
        self.connection.commit()

    def __enter__(self):
        self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()


class DbClient:
    __clients = {}
    connection = None

    def __new__(cls, client_name, client, *args, **kwargs):  # pylint: disable=unused-argument
        if client_name not in DbClient.__clients:
            DbClient.__clients[client_name] = client.connect()

        return DbClient.__clients[client_name]

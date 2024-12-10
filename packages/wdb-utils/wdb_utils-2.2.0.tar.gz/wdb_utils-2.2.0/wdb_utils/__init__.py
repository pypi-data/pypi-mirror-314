import pandas as pd
import yaml
import getpass
import os
from pathlib import Path
from importlib import import_module
from contextlib import contextmanager


class DatabaseConnection:

    def __init__(self, config_file=None):
        if pd.isnull(config_file):
            config = os.path.join(Path.home(), 'configs', 'config-default.yml')
        else:
            config = config_file
        if not os.path.exists(config):
            raise Exception('Config file not found {}'.format(config))
        with open(config, 'r') as ymlfile:
            self.config = yaml.load(ymlfile, yaml.FullLoader)

    @contextmanager
    def _connect(self):
        connection = self._create_connection()
        try:
            yield connection
        except Exception as e:
            print('Error creating database connection: {}'.format(e))

    def run_query(self, query, arraysize=120000, fetch_ct=1000000):
        results = []
        cols = None
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.arraysize = arraysize
            cursor.execute(query)
            while True:
                rows = cursor.fetchmany(fetch_ct)
                if not rows:
                    break
                else:
                    results = results + rows
            cols = [n[0] for n in cursor.description]

        if cols is not None:
            return pd.DataFrame(results, columns=cols)
        else:
            return

    def run_command(self, command):
        with self._connect() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(command)
            except Exception as e:
                print(e)
                raise e
            connection.commit()


class OracleConnection(DatabaseConnection):

    def __init__(self, config_file=None):
        self.oracledb = import_module('oracledb')
        self.oracledb.defaults.fetch_lobs = False
        super().__init__(config_file)

    def _create_connection(self):
        user = self.config['oracle']['username']
        host = self.config['oracle']['host']

        if 'password' in self.config['oracle']:
            pwd = self.config['oracle']['password']
        else:
            pwd = getpass.getpass('Database password: ')

        if 'mode' in self.config['oracle']:
            mode = self.config['oracle']['mode']
        else:
            mode = 'thin'

        try:
            if mode == 'thick':
                self.oracledb.init_oracle_client()

            conn = self.oracledb.connect(user=user, password=pwd, dsn=host)
            return conn
        except Exception as e:
            print('Error creating Oracle connection: {}'.format(e))
            return None

    def load_dataframe(self, data, schema, tablename):
        with self._connect() as connection:
            cursor = connection.cursor()
            inserted_data = [
                [None if pd.isnull(value) else value for value in sublist]
                for sublist in data.values.tolist()]
            sql = '''
             insert into {}.{} ({}
             ) values ({})
          '''.format(schema,
                     tablename,
                     ', '.join(["{}".format(colname) for colname in data.columns]),
                     ', '.join([":{}".format(x) for x in range(1, len(data.columns)+1)])
                     )
            try:
                cursor.executemany(sql, inserted_data)
                connection.commit()
                connection.close()

            except self.oracledb.DatabaseError as e:
                print(e)
                connection.rollback()
                connection.close()
                raise e


class SnowflakeConnection(DatabaseConnection):

    def __init__(self, config_file=None):
        super().__init__(config_file)
        self.snow_connect = import_module('snowflake.connector')

    def _create_connection(self):
        self.snow_connect.paramstyle = 'numeric'

        if 'password' in self.config['snowflake']:
            pwd = self.config['snowflake']['password']
        else:
            pwd = getpass.getpass('Database password: ')

        try:
            conn = self.snow_connect.connect(
                user=self.config['snowflake']['username'],
                password=pwd,
                account=self.config['snowflake']['account'],
                database=self.config['snowflake']['database'],
                schema=self.config['snowflake']['schema']
            )
            return conn
        except Exception as e:
            print('Error creating Snowflake connection: {}'.format(e))
            return None

    def load_dataframe(self, data, schema, tablename):
        from snowflake.connector.pandas_tools import write_pandas
        data.columns = map(lambda x: str(x).upper(), data.columns)
        with self._connect() as connection:
            try:
                write_pandas(connection, data, tablename, schema=schema)
            except Exception as e:
                print(e)
                raise e


def run_query_oracle(q, config=None):
    c = OracleConnection(config)
    return c.run_query(q)


def run_command_oracle(command, config=None):
    c = OracleConnection(config)
    return c.run_command(command)


def load_data_oracle(data, schema, tablename, config=None):
    c = OracleConnection(config)
    return c.load_dataframe(data, schema, tablename)


def run_query_snowflake(q, config=None):
    c = SnowflakeConnection(config)
    return c.run_query(q)


def run_command_snowflake(command, config=None):
    c = SnowflakeConnection(config)
    return c.run_command(command)


def load_data_snowflake(data, schema, tablename, config=None):
    c = SnowflakeConnection(config)
    return c.load_dataframe(data, schema, tablename)


def run_query(q, config=None):
    return run_query_oracle(q, config)


def run_command(q, config=None):
    return run_command_oracle(q, config)


def load_data(data, schema, tablename, config=None):
    return load_data_oracle(data, schema, tablename, config)

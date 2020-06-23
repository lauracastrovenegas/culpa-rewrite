import os
import unittest

from api.app import create_app
from api.config import configs
from api.data import db


class LoadersBaseTest(unittest.TestCase):
    MYSQL_DATABASE_DB = 'culpa_test'
    SCHEMA_FILE = '../databases/schema.sql'
    SCHEMA_PATH = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), SCHEMA_FILE)

    def setUp(self):
        '''
        Creates fresh database from SQL Schema file for each test case. It is
        necessary that the Schema file always remains up to date with the
        live db.
        '''
        app = create_app(configs['testing'])

        # initialize db
        with app.app_context():
            conn = db.get_db()

            # Test database should not exist
            conn.cursor().execute(f'CREATE DATABASE {self.MYSQL_DATABASE_DB}')
            conn.select_db(self.MYSQL_DATABASE_DB)
            with open(self.SCHEMA_PATH, 'r') as f:
                queries = f.read().split(';')

                # remove the last item from list due to newline and EOF
                queries.pop()

                for query in queries:
                    conn.cursor().execute(query)

        # change config so that future connections use the newly created db
        app.config['MYSQL_DATABASE_DB'] = self.MYSQL_DATABASE_DB

        self.app = app.test_client()
        self.app_ctx = app.app_context()
        self.app_ctx.push()

    def tearDown(self):
        '''
        Drops test database and pops flask app context
        '''
        db.get_cursor().execute(
            f'DROP DATABASE IF EXISTS {self.MYSQL_DATABASE_DB}'
        )
        self.app_ctx.pop()

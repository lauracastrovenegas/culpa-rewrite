from werkzeug.security import generate_password_hash

from api.data import db
from api.data.users_loaders import load_user
from api.tests import LoadersBaseTest


class UsersLoadersTest(LoadersBaseTest):
    def test_load_user(self):
        cur = db.get_cursor()
        password = 'taxthestudents'
        phash = generate_password_hash(password)
        cur.execute(
            'INSERT INTO users (email, username, password, privileges)'
            'VALUES (%s, %s, %s, %s)',
            ['lcb50@columbia.edu', 'theBigL', phash, '']
        )
        expected_res = [{'users_id': 1,
                         'email': 'lcb50@columbia.edu',
                         'username': 'theBigL',
                         'password': phash,
                         'privileges': ''
                         }]

        res = load_user('theBigL')

        self.assertEqual(expected_res, res)

    def test_load_missing_user(self):
        res = load_user('theBigL')
        self.assertEqual(res, ())

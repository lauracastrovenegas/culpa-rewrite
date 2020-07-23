from api.data import db
from api.data.professor_loaders import get_all_professors
from api.tests import LoadersBaseTest


class ProfessorLoadersTest(LoadersBaseTest):
    def test_load_professors(self):
        cur = db.get_cursor()
        cur.execute(
            'INSERT INTO professor (first_name, last_name)'
            'VALUES ("test1", "test1")'
        )
        expected_res = [{'id': 1,
                         'first_name': 'test1',
                         'last_name': 'test1'
                         }]

        res = get_all_professors()

        self.assertEqual(expected_res, res)

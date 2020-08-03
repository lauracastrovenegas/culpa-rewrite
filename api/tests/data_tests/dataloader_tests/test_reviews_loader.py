import datetime
from unittest import mock

from pymysql.err import IntegrityError

from api.data import db
from api.data.dataloaders.reviews_loader import insert_review
from api.tests import LoadersBaseTest
from api.tests.data_tests.dataloader_tests.common import \
    setup_department_professor_courses

NOW = datetime.datetime.utcnow().replace(microsecond=0)


class ReviewsLoaderTest(LoadersBaseTest):
    @mock.patch('api.data.dataloaders.reviews_loader.datetime')
    def test_insert_valid_review(self, mock_datetime):
        mock_datetime.datetime.utcnow.return_value = NOW
        cur = db.get_cursor()
        setup_department_professor_courses(cur)

        insert_review(1, 'gr8 class verma', 'i luv ml', 5)

        cur.execute(
            'SELECT * FROM review WHERE review.review_id = 1'
        )
        results = cur.fetchall()

        expected_res = {
            'review_id': 1,
            'course_professor_id': 1,
            'content': 'gr8 class verma',
            'workload': 'i luv ml',
            'rating': 5,
            'submission_date': NOW
        }
        self.assertEqual(len(results), 1)
        self.assertEqual(expected_res, results[0])

    @mock.patch('api.data.dataloaders.reviews_loader.datetime')
    def test_insert_review_with_invalid_course_professor(self, mock_datetime):
        mock_datetime.datetime.utcnow.return_value = NOW
        cur = db.get_cursor()
        setup_department_professor_courses(cur)

        # no course_professor with course_professor_id = 1000 should exist
        self.assertRaises(IntegrityError, insert_review,
                          1000, 'gr8 class that no exist', 'this is fake', 1)

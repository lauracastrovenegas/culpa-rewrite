from datetime import datetime, timedelta
from decimal import Decimal

from api.tests import LoadersWritersBaseTest
from api.tests.data_tests.common import setup_votes, setup_reviews
from api.data.dataloaders.reviews_loader import get_reviews_by_page_attr, \
    prepare_course_query_prefix, prepare_professor_query_prefix


class ReviewsLoaderTest(LoadersWritersBaseTest):
    def test_get_reviews_by_page_attr_get_only(self):
        test_cases = [{
            'type': 'course',
            'id': 4,
            'expected_res': [{
                'professor_id': 3,
                'first_name': 'Jae W',
                'last_name': 'Lee',
                'uni': 'jwl3',
                'review_id': 4,
                'content': 'demo content 4',
                'workload': 'demo workload 4',
                'rating': 3,
                'submission_date': datetime.strptime('2019-10-13', '%Y-%m-%d'),
                'agrees': Decimal(0),
                'disagrees': Decimal(0),
                'funnys': Decimal(0),
                'agree_clicked': Decimal(0),
                'disagree_clicked': Decimal(0),
                'funny_clicked': Decimal(0)
            }, {
                'professor_id': 3,
                'first_name': 'Jae W',
                'last_name': 'Lee',
                'uni': 'jwl3',
                'review_id': 5,
                'content': 'demo content 5',
                'workload': 'demo workload 5',
                'rating': 3,
                'submission_date': datetime.strptime('2018-09-01', '%Y-%m-%d'),
                'agrees': Decimal(1),
                'disagrees': Decimal(2),
                'funnys': Decimal(1),
                'agree_clicked': Decimal(0),
                'disagree_clicked': Decimal(1),
                'funny_clicked': Decimal(1)
            }, {
                'professor_id': 3,
                'first_name': 'Jae W',
                'last_name': 'Lee',
                'uni': 'jwl3',
                'review_id': 6,
                'content': 'demo content 6',
                'workload': 'demo workload 6',
                'rating': 3,
                'submission_date': datetime.strptime('2016-05-20', '%Y-%m-%d'),
                'agrees': Decimal(0),
                'disagrees': Decimal(0),
                'funnys': Decimal(0),
                'agree_clicked': Decimal(0),
                'disagree_clicked': Decimal(0),
                'funny_clicked': Decimal(0)
            }]
        }, {
            'type': 'professor',
            'id': 1,
            'expected_res': [{
                'course_id': 2,
                'call_number': 'COMS 4774',
                'name': 'Advanced Machine Learning',
                'review_id': 1,
                'content': 'demo content 1',
                'workload': 'demo workload 1',
                'rating': 3,
                'submission_date': datetime.strptime('2020-02-10', '%Y-%m-%d'),
                'agrees': Decimal(1),
                'disagrees': Decimal(1),
                'funnys': Decimal(0),
                'agree_clicked': Decimal(1),
                'disagree_clicked': Decimal(0),
                'funny_clicked': Decimal(0)
            }, {
                'course_id': 2,
                'call_number': 'COMS 4774',
                'name': 'Advanced Machine Learning',
                'review_id': 2,
                'content': 'demo content 2',
                'workload': 'demo workload 2',
                'rating': 3,
                'submission_date': datetime.strptime('2017-02-10', '%Y-%m-%d'),
                'agrees': Decimal(0),
                'disagrees': Decimal(0),
                'funnys': Decimal(1),
                'agree_clicked': Decimal(0),
                'disagree_clicked': Decimal(0),
                'funny_clicked': Decimal(1)
            }, {
                'course_id': 6,
                'call_number': 'MATH FAKE',
                'name': 'Mathematics of Machine Learning',
                'review_id': 3,
                'content': 'demo content 3',
                'workload': 'demo workload 3',
                'rating': 3,
                'submission_date': datetime.strptime('2015-02-10', '%Y-%m-%d'),
                'agrees': Decimal(2),
                'disagrees': Decimal(0),
                'funnys': Decimal(1),
                'agree_clicked': Decimal(1),
                'disagree_clicked': Decimal(0),
                'funny_clicked': Decimal(0)
            }]
        }, {
            'type': 'professor',
            'id': 12345,
            'expected_res': ()
        }, {
            'type': 'course',
            'id': 56789,
            'expected_res': ()
        }]

        ip = '123.456.78.910'
        setup_votes(self.cur)
        page_type_and_prefix_loaders = {
            'course': prepare_course_query_prefix,
            'professor': prepare_professor_query_prefix
        }

        for test_case in test_cases:
            with self.subTest(test_case):
                pf = page_type_and_prefix_loaders[test_case['type']](
                    test_case['id']
                )
                res = get_reviews_by_page_attr(pf, ip)
                self.assertEqual(res, test_case['expected_res'])

    def test_get_review_db_with_sort(self):
        def is_sorted(res, key, order):
            key_to_field_map = {
                'rating': 'rating',
                'submission_date': 'submission_date',
                'upvotes': 'agrees',
                'downvotes': 'disagrees'
            }
            field = key_to_field_map[key]
            for i in range(len(res) - 1):
                if order == 'DESC':
                    if res[i][field] < res[i + 1][field]:
                        return False
                else:
                    if res[i][field] > res[i + 1][field]:
                        return False
            return True

        setup_reviews(self.cur)
        for sort_criterion in [
            'rating',
            'submission_date',
            'upvotes',
            'downvotes'
        ]:
            for sort_order in ['DESC', 'ASC']:
                with self.subTest(
                    sort_criterion=sort_criterion,
                    sort_order=sort_order
                ):
                    res = get_reviews_by_page_attr(
                        prepare_professor_query_prefix(3),
                        "123.456.78.910",
                        sort_criterion=sort_criterion,
                        sort_order=sort_order
                    )
                    self.assertEqual(
                        is_sorted(res, sort_criterion, sort_order),
                        True
                    )

    def test_get_review_db_with_filter_year(self):
        def filter_year_correct(res, year):
            for item in res:
                if (
                    datetime.utcnow() - item['submission_date']
                ) / timedelta(days=1) > year * 365:
                    return False
            return True

        setup_reviews(self.cur)
        for year in range(1, 6):
            with self.subTest(year):
                res = get_reviews_by_page_attr(
                    prepare_professor_query_prefix(3),
                    "123.456.78.910",
                    filter_year=year
                )
                self.assertEqual(
                    filter_year_correct(res, year),
                    True
                )

    def test_get_review_db_with_filter_list(self):
        test_cases = [{
            'type': 'professor',
            'id': 3,
            'filter_list': [4, 5],
            'expected_review_ids': [4, 5, 6]
        }, {
            'type': 'professor',
            'id': 3,
            'filter_list': [1, 2, 3],
            'expected_review_ids': []
        }, {
            'type': 'course',
            'id': 2,
            'filter_list': [1],
            'expected_review_ids': [1, 2]
        }, {
            'type': 'course',
            'id': 4,
            'filter_list': [1, 2],
            'expected_review_ids': []
        }]

        setup_reviews(self.cur)
        page_type_and_prefix_loaders = {
            'course': prepare_course_query_prefix,
            'professor': prepare_professor_query_prefix
        }

        for test_case in test_cases:
            with self.subTest(test_case):
                res = get_reviews_by_page_attr(
                    page_type_and_prefix_loaders[test_case['type']](
                        test_case['id'],
                        filter_list=test_case['filter_list']
                    ),
                    "123.456.78.910"
                )
                self.assertEqual(
                    [x['review_id'] for x in res],
                    test_case['expected_review_ids']
                )

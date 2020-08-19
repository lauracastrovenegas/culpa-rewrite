from unittest import mock
from datetime import datetime

from pymysql.err import IntegrityError

from api.blueprints.review import parse_review
from api.tests import BaseTest


class ReviewTest(BaseTest):
    @mock.patch('api.blueprints.review.insert_review')
    def test_insert_valid_review(self, mock_insert_review):
        mock_insert_review.return_value = 0

        review_data = {
            'course': 99,
            'content': 'perceptrons! svms! neural networks! HMMs!',
            'workload': 'death by homework or teammates',
            'evaluation': 5,
        }

        expected_res = {'reviewId': 0}

        res = self.client.post('/api/review/submit',
                               json=review_data,
                               environ_base={'REMOTE_ADDR': '127.0.0.1'})

        self.assertEqual(expected_res, res.json)

    @mock.patch('api.blueprints.review.insert_review')
    def test_insert_invalid_review(self, mock_insert_review):
        mock_insert_review.return_value = 0

        review_data = {
            'course': 99,
            'content': 'perceptrons! svms! neural networks! HMMs!',
            'workload': 'death by homework or teammates',
            'evaluation': 5,
        }

        expected_error = {'error': 'Missing inputs'}
        for removed_key in review_data.keys():
            with self.subTest(removed_key):
                invalid_review_data = {k: v for k, v in review_data.items()
                                       if k != removed_key}

                res = self.client.post('/api/review/submit',
                                       json=invalid_review_data,
                                       environ_base={
                                           'REMOTE_ADDR': '127.0.0.1'
                                        })

                self.assertEqual(res.status_code, 400)
                self.assertEqual(expected_error, res.json)

    @mock.patch('api.blueprints.review.insert_review',
                side_effect=IntegrityError)
    def test_insert_invalid_review_db_error(self, mock_insert_review):
        review_data = {
            'course': 99,
            'content': 'perceptrons! svms! neural networks! HMMs!',
            'workload': 'death by homework or teammates',
            'evaluation': 5,
        }

        expected_error = {'error': 'Invalid data'}

        res = self.client.post('/api/review/submit',
                               json=review_data,
                               environ_base={'REMOTE_ADDR': '127.0.0.1'})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(expected_error, res.json)

    def test_parse_review(self):
        types = [{
            'r_type': 'course',
            'header_data': {
                'professor_id': 12345,
                'uni': '12345',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            'expected_review_header': {
                'profId': 12345,
                'profFirstName': 'John',
                'profLastName': 'Doe',
                'uni': '12345'
            }
        }, {
            'r_type': 'professor',
            'header_data': {
                'course_id': 12345,
                'name': 'testtest',
                'call_number': '12345'
            },
            'expected_review_header': {
                'courseId': 12345,
                'courseName': 'testtest',
                'courseCode': '12345'
            }
        }]
        dates = [
            {
                'submission_date': datetime.strptime('2014-01-01', '%Y-%m-%d'),
                'deprecated': True
            },
            {
                'submission_date': datetime.strptime('2019-01-01', '%Y-%m-%d'),
                'deprecated': False
            },
        ]

        review = {
            'agrees': -1,
            'disagrees': -2,
            'funnys': -3,
            'agree_clicked': True,
            'disagree_clicked': False,
            'funny_clicked': False,
            'review_id': 12333,
            'content': 'test content',
            'workload': 'test workload',
        }

        for type_ in types:
            for date in dates:
                with self.subTest(type_=type_, date=date):
                    review.update(type_['header_data'])
                    review['submission_date'] = date['submission_date']

                    with self.app.app_context():
                        res = parse_review(
                            review,
                            type_['r_type'],
                        )

                    self.assertEqual(res, {
                        'reviewType': type_['r_type'],
                        'reviewHeader': type_['expected_review_header'],
                        'votes': {
                            'initUpvoteCount': review['agrees'],
                            'initDownvoteCount': review['disagrees'],
                            'initFunnyCount': review['funnys'],
                            'upvoteClicked': review['agree_clicked'],
                            'downvoteClicked': review['disagree_clicked'],
                            'funnyClicked': review['funny_clicked']
                        },
                        'submissionDate': review['submission_date'],
                        'workload': review['workload'],
                        'content': review['content'],
                        'reviewId': review['review_id'],
                        'deprecated': date['deprecated']
                    })

    @mock.patch("api.blueprints.review.prepare_professor_query_prefix")
    @mock.patch("api.blueprints.review.prepare_course_query_prefix")
    @mock.patch("api.blueprints.review.get_reviews_by_page_attr")
    def test_get_reviews_valid(
        self,
        get_reviews_by_page_attr_mock,
        course_query_prefix_mock,
        professor_query_prefix_mock
    ):
        sorting_spec = {
            '': ['submission_date', 'DESC'],
            'best': ['rating', 'DESC'],
            'worst': ['rating', 'ASC'],
            'newest': ['submission_date', 'DESC'],
            'oldest': ['submission_date', 'ASC'],
            'most agreed': ['upvotes', 'DESC'],
            'most disagreed': ['downvotes', 'DESC']
        }
        filters = [{
            'filter_list': '1,2,3,4',
            'filter_list_array': [1, 2, 3, 4],
            'filter_year': 10
        }, {
            'filter_list': '5,6,7',
            'filter_list_array': [5, 6, 7],
            'filter_year': None
        }, {
            'filter_list': '',
            'filter_list_array': None,
            'filter_year': 2
        }, {
            'filter_list': '',
            'filter_list_array': None,
            'filter_year': None
        }]
        cases = [{
            'type': 'professor',
            'id': 12345,
            'fn': professor_query_prefix_mock,
            'fn_return': 'professor_mock_fn_return'
        }, {
            'type': 'course',
            'id': 56789,
            'fn': course_query_prefix_mock,
            'fn_return': 'course_mock_fn_return'
        }]
        ip = 3, "123.456.78.910"

        for case in cases:
            for sorting in sorting_spec:
                for filter_val in filters:
                    with self.subTest(
                        case=case,
                        sorting=sorting,
                        filter_val=filter_val
                    ):
                        case['fn'].return_value = case['fn_return']
                        self.client.get(
                            f'/api/review/get/{case["type"]}/{case["id"]}'
                            f'?sorting={sorting}'
                            f'&filter_year={filter_val["filter_year"]}'
                            f'&filter_list={filter_val["filter_list"]}',
                            environ_base={'REMOTE_ADDR': ip}
                        )

                        case['fn'].assert_called_with(
                            case['id'],
                            filter_val['filter_list_array']
                        )

                        sort_criterion, sort_order = sorting_spec[sorting]
                        get_reviews_by_page_attr_mock.assert_called_with(
                            case['fn_return'],
                            ip,
                            sort_criterion,
                            sort_order,
                            filter_val['filter_year']
                        )

    @mock.patch("api.blueprints.review.prepare_professor_query_prefix")
    @mock.patch("api.blueprints.review.prepare_course_query_prefix")
    @mock.patch("api.blueprints.review.get_reviews_by_page_attr")
    def test_get_reviews_invalid_type(
        self,
        get_reviews_by_page_attr_mock,
        course_query_prefix_mock,
        professor_query_prefix_mock
    ):
        cases = [{
            'type': 'course',
            'sort': 'invalid',
            'error_msg': 'invalid sorting setting'
        }, {
            'type': 'invalid',
            'sort': '',
            'error_msg': 'invalid page type'
        }]

        for case in cases:
            with self.subTest(case):
                res = self.client.get(
                    f"/api/review/get/{case['type']}/1?sorting={case['sort']}"
                )
                self.assertEqual(res.status_code, 400)
                self.assertEqual(res.json, {"error": case['error_msg']})

                get_reviews_by_page_attr_mock.assert_not_called()
                course_query_prefix_mock.assert_not_called()
                professor_query_prefix_mock.assert_not_called()

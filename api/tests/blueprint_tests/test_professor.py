from unittest import mock
from datetime import datetime
from api.tests import BaseTest

from api.blueprints.professor import parse_professor


class ProfessorsTest(BaseTest):
    VERMA_PROFESSOR_ID = 1

    POSITIVE_REVIEW = {
        'course_id': 1,
        'call_number': 'COMS 4771',
        'name': 'Machine Learning',
        'review_id': 1,
        'content': 'demo content 1',
        'workload': 'demo workload 1',
        'rating': 5,
        'submission_date': datetime.strptime('2019-10-13', '%Y-%m-%d'),
        'agrees': 1,
        'disagrees': 2,
        'funnys': 1,
        'agree_clicked': 0,
        'disagree_clicked': 1,
        'funny_clicked': 1
    }

    NEGATIVE_REVIEW = {
        'course_id': 1,
        'call_number': 'COMS 4771',
        'name': 'Machine Learning',
        'review_id': 4,
        'content': 'demo content 4',
        'workload': 'demo workload 4',
        'rating': 1,
        'submission_date': datetime.strptime('2019-10-13', '%Y-%m-%d'),
        'agrees': 0,
        'disagrees': 0,
        'funnys': 0,
        'agree_clicked': 0,
        'disagree_clicked': 0,
        'funny_clicked': 0
    }

    POSITIVE_REVIEW_JSON = {
        'content': 'demo content 1',
        'deprecated': False,
        'reviewHeader': {
            'courseId': 1,
            'courseName': 'Machine Learning',
            'courseCallNumber': 'COMS 4771'
        },
        'reviewId': 1,
        'reviewType': 'professor',
        'submissionDate': 'Oct 13, 2019',
        'votes': {
            'downvoteClicked': True,
            'funnyClicked': True,
            'initDownvoteCount': 2,
            'initFunnyCount': 1,
            'initUpvoteCount': 1,
            'upvoteClicked': False
        },
        'workload': 'demo workload 1'
    }

    NEGATIVE_REVIEW_JSON = {
        'content': 'demo content 4',
        'deprecated': False,
        'reviewHeader': {
            'courseId': 1,
            'courseName': 'Machine Learning',
            'courseCallNumber': 'COMS 4771'
        },
        'reviewId': 4,
        'reviewType': 'professor',
        'submissionDate': 'Oct 13, 2019',
        'votes': {
            'downvoteClicked': False,
            'funnyClicked': False,
            'initDownvoteCount': 0,
            'initFunnyCount': 0,
            'initUpvoteCount': 0,
            'upvoteClicked': False
        },
        'workload': 'demo workload 4'
    }

    def test_parse_professor_with_departments_and_badges(self):
        professors = [{
            'professor_id': 1,
            'first_name': 'Nakul',
            'last_name': 'Verma',
            'department_ids': '[1, 2, 1, 2]',
            'department_names': '["Computer Science", "Mathematics", '
                              + '"Computer Science", "Mathematics"]',
            'badges': '[1, 1, 2, 2]',
        }, {
            'professor_id': 2,
            'first_name': 'Lee',
            'last_name': 'Bollinger',
            'department_ids': '[3, 3]',
            'department_names': '["Law", "Law"]',
            'badges': '[1, 2]',
        }, {
            'professor_id': 3,
            'first_name': 'Jae Woo',
            'last_name': 'Lee',
            'department_ids': '[1]',
            'department_names': '["Computer Science"]',
            'badges': '[null]',
        }]

        expected_jsons = [{
            'badges': [1, 2],
            'departments': [{
                'departmentId': 1,
                'departmentName': 'Computer Science'
            }, {
                'departmentId': 2,
                'departmentName': 'Mathematics'
            }],
            'firstName': 'Nakul',
            'lastName': 'Verma',
            'professorId': 1,
        }, {
            'badges': [1, 2],
            'departments': [{
                'departmentId': 3,
                'departmentName': 'Law'
            }],
            'firstName': 'Lee',
            'lastName': 'Bollinger',
            'professorId': 2,
        }, {
            'badges': [],
            'departments': [{
                'departmentId': 1,
                'departmentName': 'Computer Science'
            }],
            'firstName': 'Jae Woo',
            'lastName': 'Lee',
            'professorId': 3,
        }]

        for professor, expected_json in zip(professors, expected_jsons):
            professor_json = parse_professor(professor)
            self.assertEqual(professor_json, expected_json)

    def test_parse_professors_with_departments(self):
        professors = [{
            'professor_id': 1,
            'first_name': 'Nakul',
            'last_name': 'Verma',
            'department_ids': '[1, 2]',
            'department_names': '["Computer Science", "Mathematics"]'
        }, {
            'professor_id': 2,
            'first_name': 'Lee',
            'last_name': 'Bollinger',
            'department_ids': '[3]',
            'department_names': '["Law"]',
        }]

        expected_jsons = [{
            'badges': [],
            'departments': [{
                'departmentId': 1,
                'departmentName': 'Computer Science'
            }, {
                'departmentId': 2,
                'departmentName': 'Mathematics'
            }],
            'firstName': 'Nakul',
            'lastName': 'Verma',
            'professorId': 1,
        }, {
            'badges': [],
            'departments': [{
                'departmentId': 3,
                'departmentName': 'Law'
            }],
            'firstName': 'Lee',
            'lastName': 'Bollinger',
            'professorId': 2,
        }]

        for professor, expected_json in zip(professors, expected_jsons):
            professor_json = parse_professor(professor)
            self.assertEqual(professor_json, expected_json)

    def test_parse_professors_with_badges(self):
        professors = [{
            'professor_id': 1,
            'first_name': 'Nakul',
            'last_name': 'Verma',
            'badges': '[1, 2]',
        }, {
            'professor_id': 2,
            'first_name': 'Lee',
            'last_name': 'Bollinger',
            'badges': '[1]',
        }, {
            'professor_id': 3,
            'first_name': 'Jae Woo',
            'last_name': 'Lee',
            'badge_id': '[null]',
        }]

        expected_jsons = [{
            'badges': [1, 2],
            'departments': [],
            'firstName': 'Nakul',
            'lastName': 'Verma',
            'professorId': 1,
        }, {
            'badges': [1],
            'departments': [],
            'firstName': 'Lee',
            'lastName': 'Bollinger',
            'professorId': 2,
        }, {
            'badges': [],
            'departments': [],
            'firstName': 'Jae Woo',
            'lastName': 'Lee',
            'professorId': 3,
        }]

        for professor, expected_json in zip(professors, expected_jsons):
            professor_json = parse_professor(professor)
            self.assertEqual(professor_json, expected_json)

    @mock.patch('api.blueprints.professor.load_review_highlight')
    @mock.patch('api.blueprints.professor.load_professor_courses')
    @mock.patch('api.blueprints.professor.load_professor_basic_info_by_id')
    def test_get_professor_info_two_review_highlights(
            self,
            mock_load_professor_basic_info_by_id,
            mock_professor_courses,
            mock_load_review_highlight):
        mock_load_professor_basic_info_by_id.return_value = [{
            'first_name': 'Nakul',
            'last_name': 'Verma',
            'badges': '[1, 2]',
        }]
        mock_professor_courses.return_value = [{
            'course_id': 1,
            'name': 'Machine Learning',
            'call_number': 'COMS 4771'
        }, {
            'course_id': 2,
            'name': 'Advanced Machine Learning',
            'call_number': 'COMS 4774'
        }]
        mock_load_review_highlight.return_value = [
            self.POSITIVE_REVIEW,
            self.NEGATIVE_REVIEW,
        ]
        expected_res = {
            'professorSummary': {
                'firstName': 'Nakul',
                'lastName': 'Verma',
                'badges': [1, 2],
                'courses': [
                    {
                        'courseId': 1,
                        'courseName': 'Machine Learning',
                        'courseCallNumber': 'COMS 4771'
                    }, {
                        'courseId': 2,
                        'courseName': 'Advanced Machine Learning',
                        'courseCallNumber': 'COMS 4774'
                    }
                ]
            },
            'professorReviewHighlight': [
                self.POSITIVE_REVIEW_JSON,
                self.NEGATIVE_REVIEW_JSON
            ]
        }

        res = self.client.get(f'/api/professor/{self.VERMA_PROFESSOR_ID}')
        self.assertEqual(expected_res, res.json)

    @mock.patch('api.blueprints.professor.load_review_highlight')
    @mock.patch('api.blueprints.professor.load_professor_courses')
    @mock.patch('api.blueprints.professor.load_professor_basic_info_by_id')
    def test_get_professor_info_one_review_highlight(
            self,
            mock_load_professor_basic_info_by_id,
            mock_professor_courses,
            mock_load_review_highlight):
        mock_load_professor_basic_info_by_id.return_value = [{
            'first_name': 'Nakul',
            'last_name': 'Verma',
            'badges': '[1, 2]',
        }]
        mock_professor_courses.return_value = [{
            'course_id': 1,
            'name': 'Machine Learning',
            'call_number': 'COMS 4771'
        }, {
            'course_id': 2,
            'name': 'Advanced Machine Learning',
            'call_number': 'COMS 4774'
        }]
        mock_load_review_highlight.return_value = [
            self.POSITIVE_REVIEW
        ]
        expected_res = {
            'professorSummary': {
                'firstName': 'Nakul',
                'lastName': 'Verma',
                'badges': [1, 2],
                'courses': [
                    {
                        'courseId': 1,
                        'courseName': 'Machine Learning',
                        'courseCallNumber': 'COMS 4771'
                    }, {
                        'courseId': 2,
                        'courseName': 'Advanced Machine Learning',
                        'courseCallNumber': 'COMS 4774'
                    }
                ]
            },
            'professorReviewHighlight': [
                self.POSITIVE_REVIEW_JSON
            ]
        }

        res = self.client.get(f'/api/professor/{self.VERMA_PROFESSOR_ID}')
        self.assertEqual(expected_res, res.json)

    @mock.patch('api.blueprints.professor.load_review_highlight')
    @mock.patch('api.blueprints.professor.load_professor_courses')
    @mock.patch('api.blueprints.professor.load_professor_basic_info_by_id')
    def test_get_professor_info_no_review_highlights(
            self,
            mock_professor_basic_info_by_id,
            mock_professor_courses,
            mock_load_review_highlight):
        mock_professor_basic_info_by_id.return_value = [{
            'first_name': 'Nakul',
            'last_name': 'Verma',
            'badges': '[1, 2]',
        }]
        mock_professor_courses.return_value = [{
            'course_id': 1,
            'name': 'Machine Learning',
            'call_number': 'COMS 4771'
        }, {
            'course_id': 2,
            'name': 'Advanced Machine Learning',
            'call_number': 'COMS 4774'
        }]
        mock_load_review_highlight.return_value = []
        expected_res = {
            'professorSummary': {
                'firstName': 'Nakul',
                'lastName': 'Verma',
                'badges': [1, 2],
                'courses': [
                    {
                        'courseId': 1,
                        'courseName': 'Machine Learning',
                        'courseCallNumber': 'COMS 4771'
                    }, {
                        'courseId': 2,
                        'courseName': 'Advanced Machine Learning',
                        'courseCallNumber': 'COMS 4774'
                    }
                ]
            },
            'professorReviewHighlight': []
        }

        res = self.client.get(f'/api/professor/{self.VERMA_PROFESSOR_ID}')
        self.assertEqual(expected_res, res.json)

    @mock.patch('api.blueprints.professor.load_review_highlight')
    @mock.patch('api.blueprints.professor.load_professor_courses')
    @mock.patch('api.blueprints.professor.load_professor_basic_info_by_id')
    def test_get_professor_info_no_courses(
            self,
            mock_load_professor_basic_info_by_id,
            mock_professor_courses,
            mock_load_review_highlight):
        mock_load_professor_basic_info_by_id.return_value = [{
            'first_name': 'Nakul',
            'last_name': 'Verma',
            'badges': '[1, 2]',
        }]
        mock_professor_courses.return_value = []
        mock_load_review_highlight.return_value = [
            self.POSITIVE_REVIEW,
            self.NEGATIVE_REVIEW,
        ]
        expected_res = {
            'professorSummary': {
                'firstName': 'Nakul',
                'lastName': 'Verma',
                'badges': [1, 2],
                'courses': []
            },
            'professorReviewHighlight': [
                self.POSITIVE_REVIEW_JSON,
                self.NEGATIVE_REVIEW_JSON
            ]
        }

        res = self.client.get(f'/api/professor/{self.VERMA_PROFESSOR_ID}')
        self.assertEqual(expected_res, res.json)

    @mock.patch('api.blueprints.professor.load_professor_basic_info_by_id')
    def test_get_professor_info_empty(
            self,
            mock_load_professor_basic_info_by_id):
        mock_load_professor_basic_info_by_id.return_value = []
        expected_error = {'error': 'Missing professor basic info'}

        res = self.client.get(f'/api/professor/{self.VERMA_PROFESSOR_ID}')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(expected_error, res.json)

    @mock.patch('api.blueprints.professor.load_professor_courses')
    def test_get_professor_courses(self, mock_professor_courses):
        mock_professor_courses.return_value = [{
            'course_id': 1,
            'name': 'Machine Learning',
            'call_number': 'COMS 4771'
        }, {
            'course_id': 2,
            'name': 'Advanced Machine Learning',
            'call_number': 'COMS 4774'
        }]
        expected_res = {
            'courses': [
                {
                    'text': 'Machine Learning',
                    'value': 1,
                    'key': 'Machine Learning'
                }, {
                    'text': 'Advanced Machine Learning',
                    'value': 2,
                    'key': 'Advanced Machine Learning'
                }
            ]
        }

        res = self.client.get(
            f'/api/professor/{self.VERMA_PROFESSOR_ID}/courses')
        self.assertEqual(expected_res, res.json)

    @mock.patch('api.blueprints.professor.load_professor_courses')
    def test_get_professor_courses_empty(self, mock_professor_courses):
        mock_professor_courses.return_value = []
        expected_res = {
            'courses': []
        }

        res = self.client.get(
            f'/api/professor/{self.VERMA_PROFESSOR_ID}/courses')
        self.assertEqual(expected_res, res.json)

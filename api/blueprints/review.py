import flask
from datetime import datetime, timedelta

from api.data.dataloaders.courses_loader import get_cp_id_by_course, \
    get_course_by_id
from api.data.dataloaders.professors_loader import get_cp_id_by_prof, \
    get_prof_by_id
from api.data.dataloaders.reviews_loader import get_reviews_db
from api.data.datawriters.reviews_writer import insert_review

review_blueprint = flask.Blueprint('review_blueprint', __name__)


def parse_review(review, r_type, id):
    '''
    static method for parsing a review into a json object
    '''
    deprecated = (
        datetime.utcnow() - review['submission_date']
    ) / timedelta(days=1) >= 5 * 365

    try:
        if r_type == 'course':
            res = get_prof_by_id(id)
            reviewHeader = {
                'profId': res['professor_id'],
                'profFirstName': res['first_name'],
                'profLastName': res['last_name'],
                'uni': res['uni']
            }
        else:
            res = get_course_by_id(id)
            reviewHeader = {
                'courseId': res['course_id'],
                'courseName': res['name'],
                'courseCode': res['call_number']
            }

    except Exception as e:
        print(e)
        raise

    return {
            'reviewType': r_type,
            'reviewHeader': reviewHeader,
            'votes': {
                'initUpvoteCount': int(review['upvotes']),
                'initDownvoteCount': int(review['downvotes']),
                'initFunnyCount': int(review['funnys']),
                'upvoteClicked': bool(review['upvote_clicked']),
                'downvoteClicked': bool(review['downvote_clicked']),
                'funnyClicked': bool(review['funny_clicked']),
            },
            'reviewId': review['review_id'],
            'content': review['content'],
            'workload': review['workload'],
            'submissionDate': review['submission_date'],
            'deprecated': deprecated,
        }


@review_blueprint.route('/submit', methods=['POST'])
def submit_review():
    '''
    Inserts a review into the database. Even though the frontend
    passes a professor_id selected by the user, the course_professor_id
    contains all of the information needed to create a review and
    we ignore the professor_id.
    '''
    if not flask.request.is_json:
        return {'error': 'Missing JSON in request'}, 422

    request_json = flask.request.get_json()

    ip_addr = flask.request.remote_addr
    try:
        content = request_json['content']
        workload = request_json['workload']
        evaluation = request_json['evaluation']

        # the frontend name is `course` to keep consistency.
        course_professor_id = request_json['course']
    except KeyError:
        return {'error': 'Missing inputs'}, 400

    try:
        review_id = insert_review(
            course_professor_id,
            content,
            workload,
            evaluation,
            ip_addr
        )
    except Exception:
        return {'error': 'Invalid review'}, 400

    return {'reviewId': review_id}


@review_blueprint.route('/get', methods=['GET', 'POST'])
def get_reviews():
    '''
    loads reviews for a specific prof/course,
    supports sorting/filtering,
    used by both the Course/ProfessorPage (GET req through
    useDataFetch upon initial rendering) and the
    shared ReviewSection component (POST req when sorting
    and/or filtering criteria is changed)
    '''
    sorting_spec = {
        'best': ['rating', True],
        'worst': ['rating', False],
        'newest': ['submission_date', True],
        'oldest': ['submission_date', False],
        'most agreed': ['upvotes', True],
        'most disagreed': ['downvotes', True]
    }
    valid_page_types = {
        'professor': get_cp_id_by_prof,
        'course': get_cp_id_by_course
    }

    ip = flask.request.remote_addr
    url_args = flask.request.args
    body_params = flask.request.get_json()

    # getting basic information: page type
    page_type = url_args.get('type').lower()
    if page_type not in valid_page_types:
        return {
            "error": "invalid page type"
        }, 400

    # getting sorting and filtering settings
    # default: sort by date
    sort_crit, sort_desc = sorting_spec['newest']
    filter_list, filter_year = None, None
    if body_params:
        sorting = body_params.get('sorting').lower()
        filter_list = body_params.get('filterList')
        filter_year = body_params.get('filterYear')

        if sorting:
            if sorting not in sorting_spec:
                return {
                    "error": "invalid sorting setting"
                }, 400
            sort_crit, sort_desc = sorting_spec[sorting]

    try:
        cp_ids = valid_page_types[page_type](
            int(url_args.get(f'{page_type}Id')),
            filter_list
        )
        cp_id_map = {
            x['course_professor_id']: x[
                'course_id' if page_type == 'professor' else 'professor_id'
            ] for x in cp_ids
        }

        reviews = get_reviews_db(
            list(cp_id_map.keys()), ip, sort_crit, sort_desc, filter_year
        ) if cp_id_map else []

        json = [parse_review(
            review,
            page_type,
            cp_id_map[review['course_professor_id']]
        ) for review in reviews]
        return {'reviews': json}

    except Exception as e:
        # print statement for debugging
        print(e)
        return {"error": str(e)}, 500

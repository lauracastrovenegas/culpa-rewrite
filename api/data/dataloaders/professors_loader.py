from pypika import MySQLQuery as Query, Criterion, Order, \
  CustomFunction

from api.data import db
from api.data.common import badge, badge_professor, course, \
  course_professor, department, department_professor, professor, \
  Match, APPROVED

JsonArrayAgg = CustomFunction('JSON_ARRAYAGG', ['attribute'])


# TODO: This method is temporary to test search functionality
# and should be removed in the future
def get_all_professors():
    cur = db.get_cursor()
    query = Query \
        .from_(professor) \
        .select(
            professor.professor_id,
            professor.first_name,
            professor.last_name) \
        .where(
            professor.status == APPROVED) \
        .get_sql()

    cur.execute(query)
    return cur.fetchall()


# TODO: Change professor loaders to be more generic:
# Private generic functions:
#   _load_professor_by_id(professor_id, [statuses])
#   _load_professor_by_uni(professor_uni, [statuses])
#
# Public functions (e.g.):
# def load_approved_professor_by_id(professor_id):
#   return _load_professor_by_id(professor_id, APPROVED)


def load_professor_basic_info_by_id(professor_id):
    cur = db.get_cursor()
    query = Query \
        .from_(professor) \
        .left_join(badge_professor) \
        .on(badge_professor.professor_id == professor.professor_id) \
        .left_join(badge) \
        .on(badge.badge_id == badge_professor.badge_id) \
        .select(
            professor.first_name,
            professor.last_name,
            JsonArrayAgg(badge.badge_id).as_('badges')) \
        .where(Criterion.all([
            professor.professor_id == professor_id,
            professor.status == APPROVED
        ])) \
        .groupby(
            professor.first_name,
            professor.last_name) \
        .get_sql()

    cur.execute(query)
    return cur.fetchall()


def load_professor_basic_info_by_uni(professor_uni):
    cur = db.get_cursor()
    query = Query \
        .from_(professor) \
        .select(
            professor.professor_id,
            professor.first_name,
            professor.last_name,
            professor.uni,
        ) \
        .where(Criterion.all([
            professor.uni == professor_uni,
            professor.status == APPROVED
        ])) \
        .get_sql()

    cur.execute(query)
    return cur.fetchall()


def load_any_status_professor_by_uni(professor_uni):
    cur = db.get_cursor()
    query = Query \
        .from_(professor) \
        .select(
            professor.professor_id,
            professor.first_name,
            professor.last_name,
            professor.uni,
            professor.status,
        ) \
        .where(professor.uni == professor_uni) \
        .get_sql()

    cur.execute(query)
    return cur.fetchone()


def load_professor_courses(professor_id):
    '''
    Loads all of the course data for a given professor. The courses
    will be identified by `course_professor_id` since these ids are
    unique for a given professor.
    '''
    cur = db.get_cursor()
    query = Query \
        .from_(course) \
        .join(course_professor) \
        .on(
            course_professor.course_id == course.course_id) \
        .select(
            course.course_id,
            course.name,
            course.call_number) \
        .where(Criterion.all([
            course_professor.professor_id == professor_id,
            course_professor.status == APPROVED
        ])) \
        .get_sql()

    cur.execute(query)
    return cur.fetchall()


def search_professor(search_query, limit=None):
    cur = db.get_cursor()

    search_params = [param + '*' for param in search_query.split()]
    search_params = ' '.join(search_params)
    match = Match(professor.first_name,
                  professor.last_name,
                  professor.uni) \
        .against(search_params) \
        .as_('score')

    # This subquery guarantees limit == number of distinct professors
    # otherwise, limit == number of rows != number of distinct professors
    distinct_professor = Query \
        .from_(professor) \
        .select(
            'professor_id',
            'first_name',
            'last_name',
            match
        ) \
        .where(Criterion.all([
            match > 0,
            professor.status == APPROVED
        ])) \
        .orderby('score', order=Order.desc) \
        .limit(limit) \
        .as_('distinct_professor')

    # Professor must have a department -> inner join
    # Professor may not have a badge -> left join
    query = Query \
        .from_(distinct_professor) \
        .inner_join(department_professor) \
        .on(distinct_professor.professor_id ==
            department_professor.professor_id) \
        .inner_join(department) \
        .on(department_professor.department_id == department.department_id) \
        .left_join(badge_professor) \
        .on(distinct_professor.professor_id == badge_professor.professor_id) \
        .left_join(badge) \
        .on(badge_professor.badge_id == badge.badge_id) \
        .select(
            distinct_professor.professor_id,
            distinct_professor.first_name,
            distinct_professor.last_name,
            distinct_professor.score,
            department.department_id,
            department.name.as_('department_name'),
            badge.badge_id
        ) \
        .get_sql()

    cur.execute(query)
    return cur.fetchall()

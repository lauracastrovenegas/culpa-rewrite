from pypika import MySQLQuery as Query

from api.data import db
from api.data.common import course, course_professor, professor


def get_all_professors():
    cur = db.get_cursor()
    query = Query.from_(professor) \
        .select(
            professor.professor_id,
            professor.first_name,
            professor.last_name
    ).get_sql()
    cur.execute(query)
    return cur.fetchall()


def get_professor_courses(professor_id):
    '''
    Loads all of the course data for a given professor. The courses
    will be identified by `course_professor_id` since these ids are
    unique for a given professor.
    '''
    cur = db.get_cursor()
    query = Query.from_(course) \
        .join(course_professor) \
        .on(course_professor.course_id == course.course_id) \
        .select(
            course_professor.course_professor_id,
            course.name,
            course.call_number,
        ) \
        .where(course_professor.professor_id == professor_id) \
        .get_sql()
    cur.execute(query)
    return cur.fetchall()

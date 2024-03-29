import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import { Header } from "semantic-ui-react";

const propTypesCourseDisplayName = {
  as: PropTypes.oneOf(["header", "text"]),
  className: PropTypes.string,
  courseCallNumber: PropTypes.string,
  courseName: PropTypes.string.isRequired,
  size: PropTypes.oneOf(["tiny", "small", "medium", "large", "huge"]),
};

const propTypesCourseDisplayLink = {
  as: PropTypes.oneOf(["header", "text"]),
  className: PropTypes.string,
  courseCallNumber: PropTypes.string,
  courseId: PropTypes.number.isRequired,
  courseName: PropTypes.string.isRequired,
  size: PropTypes.oneOf(["tiny", "small", "medium", "large", "huge"]),
};

const defaultProps = {
  className: "",
  courseCallNumber: "",
  as: "text",
  size: "medium",
};

export function CourseDisplayName({
  as,
  className,
  courseCallNumber,
  courseName,
  size,
}) {
  const CourseName = as === "header" ? Header : "span";
  return (
    <CourseName className={className} size={size}>
      {courseCallNumber} {courseName}
    </CourseName>
  );
}

export function CourseDisplayLink({
  as,
  className,
  courseCallNumber,
  courseId,
  courseName,
  size,
}) {
  return (
    <Link to={`/course/${courseId}`}>
      <CourseDisplayName
        as={as}
        className={className}
        courseCallNumber={courseCallNumber}
        courseName={courseName}
        size={size}
      />
    </Link>
  );
}

CourseDisplayName.propTypes = propTypesCourseDisplayName;
CourseDisplayName.defaultProps = defaultProps;

CourseDisplayLink.propTypes = propTypesCourseDisplayLink;
CourseDisplayLink.defaultProps = defaultProps;

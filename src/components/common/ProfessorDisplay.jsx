import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import { Header } from "semantic-ui-react";

import Badge from "components/common/Badge";

const propTypesProfessorDisplayName = {
  as: PropTypes.oneOf(["header", "text"]),
  badges: PropTypes.arrayOf(PropTypes.number),
  className: PropTypes.string,
  firstName: PropTypes.string,
  fullName: PropTypes.string,
  lastName: PropTypes.string,
  size: PropTypes.oneOf(["tiny", "small", "medium", "large", "huge"]),
};

const propTypesProfessorDisplayLink = {
  as: PropTypes.oneOf(["header", "text"]),
  badges: PropTypes.arrayOf(PropTypes.number),
  className: PropTypes.string,
  firstName: PropTypes.string,
  fullName: PropTypes.string,
  lastName: PropTypes.string,
  professorId: PropTypes.number.isRequired,
  size: PropTypes.oneOf(["tiny", "small", "medium", "large", "huge"]),
};

const defaultProps = {
  as: "text",
  badges: [],
  className: "",
  firstName: "",
  fullName: "",
  lastName: "",
  size: "medium",
};

export function ProfessorDisplayName({
  as,
  badges,
  className,
  firstName,
  fullName,
  lastName,
  size,
}) {
  const ProfessorName = as === "header" ? Header : "span";
  return (
    <>
      <ProfessorName className={className} size={size}>
        {fullName || `${firstName} ${lastName}`}
      </ProfessorName>
      {badges.map((badgeId, index) => (
        <span key={`badge-${badgeId}`}>
          {as === "text" && index === 0 && " "}
          <Badge badgeId={badgeId} size={size} />
        </span>
      ))}
    </>
  );
}

export function ProfessorDisplayLink({
  as,
  badges,
  className,
  firstName,
  fullName,
  lastName,
  professorId,
  size,
}) {
  return (
    <>
      <Link to={`/professor/${professorId}`}>
        <ProfessorDisplayName
          as={as}
          className={className}
          firstName={firstName}
          fullName={fullName}
          lastName={lastName}
          size={size}
        />
      </Link>
      {badges.map((badgeId, index) => (
        <span key={`badge-${badgeId}`}>
          {as === "text" && index === 0 && " "}
          <Badge badgeId={badgeId} size={size} />
        </span>
      ))}
    </>
  );
}

ProfessorDisplayName.propTypes = propTypesProfessorDisplayName;
ProfessorDisplayName.defaultProps = defaultProps;

ProfessorDisplayLink.propTypes = propTypesProfessorDisplayLink;
ProfessorDisplayLink.defaultProps = defaultProps;

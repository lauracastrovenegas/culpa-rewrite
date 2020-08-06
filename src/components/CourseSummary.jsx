import PropTypes from "prop-types";
import React, { useState } from "react";
import { Icon, Accordion, Table } from "semantic-ui-react";

import { CourseDisplayName } from "components/common/CourseDisplay";
import CreateReviewButton from "components/common/CreateReviewButton";
import { ProfessorDisplayLink } from "components/common/ProfessorDisplay";

const propTypes = {
  courseId: PropTypes.number.isRequired,
  courseSummary: PropTypes.shape({
    courseName: PropTypes.string.isRequired,
    courseCallNumber: PropTypes.string.isRequired,
    departmentName: PropTypes.string.isRequired,
    associatedProfessors: PropTypes.array.isRequired,
  }).isRequired,
};

export default function CourseSummary({ courseId, courseSummary }) {
  return (
    <div>
      <CourseHeader courseId={courseId} courseSummary={courseSummary} />
      <ReviewSummary />
    </div>
  );
}

export function CourseHeader({ courseId, courseSummary }) {
  const [isActive, setActive] = useState(false);
  const {
    courseName,
    courseCallNumber,
    departmentName,
    associatedProfessors,
  } = courseSummary;

  return (
    <div>
      <h1>
        <CourseDisplayName code={courseCallNumber} name={courseName} />
      </h1>
      <h3>Department: {departmentName}</h3>

      <Accordion>
        <Accordion.Title
          active={isActive}
          as="h3"
          onClick={() => setActive(!isActive)}
        >
          <Icon name={!isActive ? "angle down" : "angle up"} />
          {!isActive ? "Show" : "Hide"} all professors who teach this course
        </Accordion.Title>
        <Accordion.Content active={isActive}>
          {associatedProfessors.map((professor) => {
            const {
              firstName,
              lastName,
              professorId,
              profDepartments,
            } = professor;
            return (
              <Table basic="very" key={professorId} textAlign="left">
                <tbody>
                  {/* this is to prevent bugs from browser inserting <tbody> */}
                  <Table.Row>
                    <Table.Cell key={professorId}>
                      <ProfessorDisplayLink
                        as="span"
                        firstName={firstName}
                        lastName={lastName}
                        professorId={professorId}
                      />
                    </Table.Cell>
                    <Table.Cell key={`${professorId}_departments`}>
                      {profDepartments.map((department, index) => {
                        const {
                          profDepartmentId,
                          profDepartmentName,
                        } = department;
                        return (
                          <span key={profDepartmentId}>
                            {profDepartmentId}: {profDepartmentName}
                            {profDepartments.length - 1 !== index ? ", " : ""}
                          </span>
                        );
                      })}
                    </Table.Cell>
                  </Table.Row>
                </tbody>
              </Table>
            );
          })}
        </Accordion.Content>
      </Accordion>

      <CreateReviewButton compact color="yellow" courseId={courseId.toString()}>
        WRITE A REVIEW FOR {courseName}
      </CreateReviewButton>
    </div>
  );
}

function ReviewSummary() {
  return "Review Summary here";
}

CourseSummary.propTypes = propTypes;
CourseHeader.propTypes = propTypes;

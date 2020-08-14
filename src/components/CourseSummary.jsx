import PropTypes from "prop-types";
import React, { useState } from "react";
import { Icon, Accordion, Table, Grid, Container } from "semantic-ui-react";

import { CourseDisplayName } from "components/common/CourseDisplay";
import CreateReviewButton from "components/common/CreateReviewButton";
import { ProfessorDisplayLink } from "components/common/ProfessorDisplay";
import ReviewCard from "components/reviews/ReviewCard";

const propTypesCourseSummary = {
  courseId: PropTypes.number.isRequired,
  courseSummary: PropTypes.shape({
    courseName: PropTypes.string.isRequired,
    courseCallNumber: PropTypes.string.isRequired,
    departmentName: PropTypes.string.isRequired,
    associatedProfessors: PropTypes.array.isRequired,
  }).isRequired,
  reviewSummary: PropTypes.shape({
    positiveReview: PropTypes.array,
    negativeReview: PropTypes.array,
  }),
};

const defaultPropsCourseSummary = {
  reviewSummary: {
    positiveReivew: {},
    negativeReview: {},
  },
};

export default function CourseSummary({
  courseId,
  courseSummary,
  reviewSummary,
}) {
  return (
    <Grid>
      <Grid.Row>
        <CourseHeader courseId={courseId} courseSummary={courseSummary} />
      </Grid.Row>
      <Grid.Row>
        <ReviewSummary reviewSummary={reviewSummary} />
      </Grid.Row>
    </Grid>
  );
}

CourseSummary.propTypes = propTypesCourseSummary;
CourseSummary.defaultProps = defaultPropsCourseSummary;

const propTypesCourseHeader = {
  courseId: PropTypes.number.isRequired,
  courseSummary: PropTypes.shape({
    courseName: PropTypes.string.isRequired,
    courseCallNumber: PropTypes.string.isRequired,
    departmentName: PropTypes.string.isRequired,
    associatedProfessors: PropTypes.array.isRequired,
  }).isRequired,
};

export function CourseHeader({ courseId, courseSummary }) {
  const [isAccordionActive, setAccordionActive] = useState(false);
  const {
    courseName,
    courseCallNumber,
    departmentName,
    associatedProfessors,
  } = courseSummary;

  const displayAccordion = associatedProfessors.length > 5;

  const ProfessorAccordion = (
    <Accordion>
      <Accordion.Title
        active={isAccordionActive}
        as="h3"
        onClick={() => setAccordionActive(!isAccordionActive)}
      >
        <Icon name={!isAccordionActive ? "angle down" : "angle up"} />
        {!isAccordionActive ? "Show" : "Hide"} all professors who teach this
        course
      </Accordion.Title>
      <Accordion.Content active={isAccordionActive}>
        <Table basic="very" textAlign="left">
          <tbody>
            {/* this is to prevent bugs from browser inserting <tbody> */}
            {associatedProfessors.map((professor) => {
              const {
                firstName,
                lastName,
                professorId,
                profDepartments,
              } = professor;
              return (
                <Table.Row key={professorId}>
                  <Table.Cell key={professorId}>
                    <ProfessorDisplayLink
                      as="h5"
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
              );
            })}
          </tbody>
        </Table>
      </Accordion.Content>
    </Accordion>
  );

  const ProfessorList = (
    <h3>
      Professors:{" "}
      {associatedProfessors.map((professor, index) => {
        const { firstName, lastName, professorId } = professor;
        return (
          <span key={`${lastName}_${professorId}`}>
            <ProfessorDisplayLink
              as="span"
              firstName={firstName}
              lastName={lastName}
              professorId={professorId}
            />
            {associatedProfessors.length - 1 !== index ? ", " : ""}
          </span>
        );
      })}
    </h3>
  );

  return (
    <Container>
      <h1>
        <CourseDisplayName code={courseCallNumber} name={courseName} />
      </h1>
      <h3>Department: {departmentName}</h3>

      {displayAccordion ? ProfessorAccordion : ProfessorList}

      <CreateReviewButton compact color="yellow" courseId={courseId.toString()}>
        WRITE A REVIEW FOR {courseName}
      </CreateReviewButton>
    </Container>
  );
}

CourseHeader.propTypes = propTypesCourseHeader;

const propTypesReviewSummary = {
  reviewSummary: PropTypes.shape({
    positiveReview: PropTypes.array,
    negativeReview: PropTypes.array,
  }),
};

const defaultPropsReviewSummary = {
  reviewSummary: {
    positiveReivew: {},
    negativeReview: {},
  },
};

function ReviewSummary({ reviewSummary }) {
  const { positiveReview, negativeReview } = reviewSummary;

  if (positiveReview && negativeReview) {
    return (
      <Container>
        <Grid>
          <Grid.Row>
            <Grid.Column width={7}>
              <h3>Most Positive Review</h3>
              <CourseReviewCard review={positiveReview} />
            </Grid.Column>
            <Grid.Column width={1} />
            <Grid.Column width={7}>
              <h3>Most Negative Review</h3>
              <CourseReviewCard review={negativeReview} />
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Container>
    );
  }

  if (positiveReview) {
    return (
      <Container>
        <Grid>
          <Grid.Row>
            <Grid.Column width={14}>
              <h3>Most Positive Review</h3>
              <CourseReviewCard review={positiveReview} />
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Container>
    );
  }

  if (negativeReview) {
    return (
      <Container>
        <Grid>
          <Grid.Row>
            <Grid.Column width={14}>
              <h3>Most Negative Review</h3>
              <CourseReviewCard review={negativeReview} />
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Container>
    );
  }

  return "";
}

ReviewSummary.propTypes = propTypesReviewSummary;
ReviewSummary.defaultProps = defaultPropsReviewSummary;

function CourseReviewCard({ review }) {
  const {
    reviewType,
    reviewHeader,
    votes,
    workload,
    submissionDate,
    reviewId,
    deprecated,
    content,
  } = review;

  return (
    <ReviewCard
      content={content}
      deprecated={deprecated}
      reviewHeader={reviewHeader}
      reviewId={reviewId}
      reviewType={reviewType}
      submissionDate={submissionDate}
      votes={votes}
      workload={workload}
    />
  );
}

import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import { Header, List } from "semantic-ui-react";

import ErrorComponent from "components/common/ErrorComponent";
import LoadingComponent from "components/common/LoadingComponent";
import useDataFetch from "components/common/useDataFetch";

const propTypes = {
  departments: PropTypes.arrayOf(
    PropTypes.shape({
      departmentId: PropTypes.number.isRequired,
      departmentName: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
};

export function Departments({ departments }) {
  return (
    // TODO: Add styling into two columns with alphabetical sections
    <div>
      <Header>List of Departments</Header>
      <List>
        {departments.map(({ departmentId, departmentName }) => {
          return (
            <List.Item key={departmentId}>
              <Link to={{ pathname: `/department/${departmentId}` }}>{departmentName}</Link>
            </List.Item>
          );
        })}
      </List>
    </div>
  );
}

export default function DepartmentsPage() {
  const {
    data: { departments },
    isLoading,
    isError,
  } = useDataFetch("/api/departments/all", {
    departments: [],
  });

  if (isLoading || isError) {
    return isLoading ? <LoadingComponent /> : <ErrorComponent />;
  }

  return <Departments departments={departments} />;
}

Departments.propTypes = propTypes;

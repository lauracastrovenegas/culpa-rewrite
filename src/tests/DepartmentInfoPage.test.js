import { render } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { AuthContext } from "components/common/Authentication";
import DepartmentInfoPage from "components/DepartmentInfoPage";

describe("DepartmentInfoPage Component", () => {
  const loginSuccess = jest.fn(() => {
    Promise.resolve();
  });
  const testCases = [
    {
      name: "renders no info",
      departmentName: "",
      departmentCourses: [{}],
      departmentProfessors: [{}],
    },
    {
      name: "renders department info",
      departmentName: "Computer Science",
      departmentCourses: [
        {
          courseId: 1,
          courseName: "User Interface Design",
        },
        {
          courseId: 2,
          courseName: "Machine Learning",
        },
      ],
      departmentProfessors: [
        {
          professorId: 1,
          firstName: "Lydia",
          lastName: "Chilton",
        },
        {
          professorId: 2,
          firstName: "Nakul",
          lastName: "Verma",
        },
      ],
    },
  ];
  testCases.forEach(
    ({ name, departmentName, departmentCourses, departmentProfessors }) => {
      test(name, () => {
        const snapshot = render(
          <MemoryRouter>
            <AuthContext.Provider value={{ login: loginSuccess }}>
              <DepartmentInfoPage
                departmentCourses={departmentCourses}
                departmentName={departmentName}
                departmentProfessors={departmentProfessors}
              />
            </AuthContext.Provider>
          </MemoryRouter>
        );
        expect(snapshot).toMatchSnapshot();
      });
    }
  );
});

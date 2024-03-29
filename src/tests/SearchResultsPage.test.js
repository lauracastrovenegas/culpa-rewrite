import { render } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import useDataFetch from "components/common/useDataFetch";
import SearchResultsPage from "components/SearchResultsPage";

jest.mock("../components/common/useDataFetch");

afterEach(() => {
  useDataFetch.mockReset();
});

describe("SearchResultsPage Components", () => {
  const testCases = [
    {
      name: "both professors and courses found",
      testProfessorResults: [
        {
          badges: [1, 2],
          childKey: "professor-2339",
          departments: [
            {
              id: 29,
              name: "Computer Science",
            },
          ],
          id: 2339,
          title: "Nakul Verma",
          type: "professor",
        },
        {
          badges: [],
          childKey: "professor-40",
          departments: [
            {
              id: 29,
              name: "Computer Science",
            },
          ],
          last: "true",
          id: 40,
          title: "Lydia Chilton",
          type: "professor",
        },
      ],
      testCourseResults: [
        {
          childKey: "course-1",
          departments: [
            {
              id: 6,
              name: "Computer Science",
            },
          ],
          id: 1,
          title: "User Interface Design",
          type: "course",
        },
        {
          childKey: "course-2",
          departments: [
            {
              id: 6,
              name: "Computer Science",
            },
          ],
          id: 2,
          title: "Machine Learning",
          type: "course",
        },
      ],
    },
    {
      name: "only professors found",
      testProfessorResults: [
        {
          badges: [1, 2],
          childKey: "professor-2339",
          departments: [
            {
              id: 29,
              name: "Computer Science",
            },
          ],
          last: "false",
          id: 2339,
          title: "Nakul Verma",
          type: "professor",
        },
        {
          badges: [],
          childKey: "professor-40",
          departments: [
            {
              id: 29,
              name: "Computer Science",
            },
          ],
          last: "true",
          id: 40,
          title: "Lydia Chilton",
          type: "professor",
        },
      ],
      testCourseResults: [],
    },
    {
      name: "only courses found",
      testProfessorResults: [],
      testCourseResults: [
        {
          childKey: "course-1",
          departments: [
            {
              id: 6,
              name: "Computer Science",
            },
          ],
          id: 1,
          title: "User Interface Design",
          type: "course",
        },
        {
          childKey: "course-2",
          departments: [
            {
              id: 6,
              name: "Computer Science",
            },
          ],
          id: 2,
          title: "Machine Learning",
          type: "course",
        },
      ],
    },
    {
      name: "no results found",
      testProfessorResults: [],
      testCourseResults: [],
    },
  ];

  testCases.forEach(({ name, testProfessorResults, testCourseResults }) => {
    test(name, () => {
      useDataFetch.mockImplementation(() => ({
        data: {
          professorResults: testProfessorResults,
          courseResults: testCourseResults,
        },
        isError: false,
        isLoading: false,
      }));
      const snapshot = render(
        <MemoryRouter>
          <SearchResultsPage />
        </MemoryRouter>
      );
      expect(snapshot).toMatchSnapshot();
      expect(useDataFetch).toHaveBeenCalledTimes(1);
    });
  });
});

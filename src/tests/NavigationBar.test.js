import { render, fireEvent, act, screen } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { AuthProvider } from "components/common/Authentication";
import NavigationBar from "components/NavigationBar";

describe("Navbar Component Tests", () => {
  const professorAndCourseResults = {
    professorResults: [
      {
        badge: "Silver", // TODO: Update to list of badge id
        departments: [
          {
            id: 29,
            name: "Computer Science",
          },
        ],
        firstname: "Nakul",
        last: "false",
        lastname: "Verma",
        id: 2339,
        title: "Nakul Verma",
        type: "professor",
      },
    ],
    courseResults: [
      {
        id: 1,
        name: "User Interface Design",
        department: {
          id: 6,
          name: "Computer Science",
        },
        title: "User Interface Design",
      },
    ],
  };

  const onlyProfessorResults = {
    professorResults: [
      {
        badge: "Silver", // TODO: Update to list of badge id
        departments: [
          {
            id: 29,
            name: "Computer Science",
          },
        ],
        firstname: "Nakul",
        last: "false",
        lastname: "Verma",
        id: 2339,
        title: "Nakul Verma",
        type: "professor",
      },
    ],
    courseResults: [],
  };

  const onlyCourseResults = {
    professorResults: [],
    courseResults: [
      {
        id: 1,
        name: "User Interface Design",
        department: {
          id: 6,
          name: "Computer Science",
        },
        title: "User Interface Design",
      },
    ],
  };

  const noResults = {
    professorResults: [],
    courseResults: [],
  };

  const serverFoundProfessorAndCourseResults = () =>
    Promise.resolve({
      ok: true,
      json: () => professorAndCourseResults,
    });

  const serverFoundOnlyProfessorResults = () =>
    Promise.resolve({
      ok: true,
      json: () => onlyProfessorResults,
    });

  const serverFoundOnlyCourseResults = () =>
    Promise.resolve({
      ok: true,
      json: () => onlyCourseResults,
    });

  const serverFoundNoResults = () =>
    Promise.resolve({
      ok: true,
      json: () => noResults,
    });

  test("should render", () => {
    const snapshot = render(
      <AuthProvider>
        <MemoryRouter>
          <NavigationBar />
        </MemoryRouter>
      </AuthProvider>
    );
    expect(snapshot).toMatchSnapshot();
  });

  describe("searchbar interactions", () => {
    let mockFetch;

    beforeEach(() => {
      mockFetch = jest.spyOn(global, "fetch");
      render(
        <AuthProvider>
          <MemoryRouter>
            <NavigationBar />
          </MemoryRouter>
        </AuthProvider>
      );
    });

    afterEach(() => jest.resetAllMocks());

    test("both professor and course results found", async () => {
      mockFetch.mockImplementation(serverFoundProfessorAndCourseResults);

      await act(async () => {
        fireEvent.input(screen.getByRole("textbox"), {
          target: { value: "testSearchValue" },
        });
      });

      expect(await screen.getByText(/nakul verma/i)).toBeInTheDocument();
      expect(
        await screen.getByText(/user interface design/i)
      ).toBeInTheDocument();
      expect(mockFetch).toHaveBeenCalledWith(
        "/api/search?entity=all&query=testSearchValue",
        {
          method: "GET",
          headers: { "Content-Type": "Application/json" },
        }
      );
    });

    test("only professor results found", async () => {
      mockFetch.mockImplementation(serverFoundOnlyProfessorResults);

      await act(async () => {
        fireEvent.input(screen.getByRole("textbox"), {
          target: { value: "testSearchValue" },
        });
      });

      expect(await screen.getByText(/nakul verma/i)).toBeInTheDocument();
      expect(
        await screen.queryByText(/user interface design/i)
      ).not.toBeInTheDocument();
      expect(mockFetch).toHaveBeenCalledWith(
        "/api/search?entity=all&query=testSearchValue",
        {
          method: "GET",
          headers: { "Content-Type": "Application/json" },
        }
      );
    });

    test("only course results found", async () => {
      mockFetch.mockImplementation(serverFoundOnlyCourseResults);

      await act(async () => {
        fireEvent.input(screen.getByRole("textbox"), {
          target: { value: "testSearchValue" },
        });
      });

      expect(await screen.queryByText(/nakul verma/i)).not.toBeInTheDocument();
      expect(
        await screen.getByText(/user interface design/i)
      ).toBeInTheDocument();
      expect(mockFetch).toHaveBeenCalledWith(
        "/api/search?entity=all&query=testSearchValue",
        {
          method: "GET",
          headers: { "Content-Type": "Application/json" },
        }
      );
    });

    test("no results found", async () => {
      mockFetch.mockImplementation(serverFoundNoResults);

      await act(async () => {
        fireEvent.input(screen.getByRole("textbox"), {
          target: { value: "testSearchValue" },
        });
      });

      expect(await screen.queryByText(/nakul verma/i)).not.toBeInTheDocument();
      expect(
        await screen.queryByText(/user interface design/i)
      ).not.toBeInTheDocument();
      expect(mockFetch).toHaveBeenCalledWith(
        "/api/search?entity=all&query=testSearchValue",
        {
          method: "GET",
          headers: { "Content-Type": "Application/json" },
        }
      );
    });
  });
});

// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import "mutationobserver-shim";
import "@testing-library/jest-dom/extend-expect";

// Throws errors on prop type mismatches
beforeEach(() => {
  jest.spyOn(console, "error");
  jest.spyOn(console, "warn");
});

afterEach(() => {
  /* eslint-disable no-console */
  expect(console.warn).not.toBeCalled();
  expect(console.error).not.toBeCalled();
});

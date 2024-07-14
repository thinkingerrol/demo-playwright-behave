Feature: End to end

  As a developer,
  I want to make sure that my website passes a basic e2e smoke test.

  Scenario: Website is working
    When I open the url https://playwright.dev
    Then "Playwright enables reliable end-to-end testing for modern web apps." is visible on the page

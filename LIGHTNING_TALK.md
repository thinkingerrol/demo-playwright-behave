Hi everyone,
I’d like to share my experience with **Playwright** and **Behave** for E2E testing—a combination I’ve found incredibly effective and enjoyable.

I first discovered Playwright at **PyMunich** 1.5 years ago and have been using it at work ever since.
**Behave**, on the other hand, has been our trusted test runner for years.
It allows writing tests in plain-English **Given/When/Then** syntax, also known as the Gherkin language.

To help others get started, I’ve distilled how we use these tools into a tiny GitHub repo:

https://github.com/thinkingerrol/demo-playwright-behave

What I love most about both Playwright and Behave is their **simplicity and low barrier to entry**.
They’re **batteries-included**, meaning they’re my only two dependencies and bring very few transitives.
Both tools also feature **automatic code generation**, making it easy to implement **black-box E2E tests** that build confidence.

Playwright, in particular, stands out with its **debugging and reporting** features.
In our CI system, we collect **time-travel-enabling traces of failed tests** and **videos of all tests**, which are incredibly helpful.
We’ve even added **subtitles** to these videos, based on the Given/When/Then steps,
transforming them into **living documentation** for complex web apps.

To make results easy to review, we systematically name test videos by their **execution order**, **pass/fail status**, and **feature/scenario name**, making CI results clear at a glance.
Combined with the plain-English syntax of test scenarios, these tools foster seamless **collaboration between technical and non-technical stakeholders**.

In summary, this stack brings **confidence, simplicity, and collaboration** to E2E testing.
I highly recommend giving it a try. Thanks for listening!

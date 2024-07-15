# demo-playwright-behave
A tiny but working example e2e test suite using Playwright/python with behave interpreting a Gherkin feature file

# Quick start

Dockerized:
```bash
./build.sh
```

Direct (first install the dependencies as done in Dockerfile):
```bash
behave test --no-capture
```

# Integration into CI systems

If you use Jenkins, the Jenkinsfile might look like this:

```Jenkinsfile
try {
  sh './build.sh'
}
finally {
  archiveArtifacts 'build/**/*'
}
```

in the Build Artifacts you should then see files like:
* 00001__passed__end_to_end.feature__Website_is_working.webm

or:
* 00001__failed__end_to_end.feature__Website_is_working.webm

# Example output

```bash
@thinkingerrol ➜ /workspaces/demo-playwright-behave (main) $ ./build.sh
+ mkdir -p build
+ CONTAINER=playwright-e2e
+ IMAGE=playwright-e2e-local
+ echo 'Building image: playwright-e2e-local'
Building image: playwright-e2e-local
+ docker build test --tag playwright-e2e-local
[+] Building 55.8s (11/11) FINISHED                                                                                                                                        docker:default
 => [internal] load build definition from Dockerfile                                                                                                                                 0.4s
 => => transferring dockerfile: 405B                                                                                                                                                 0.0s
 => [internal] load metadata for mcr.microsoft.com/playwright/python:v1.36.0-jammy-amd64                                                                                             0.7s
 => [internal] load .dockerignore                                                                                                                                                    0.2s
 => => transferring context: 2B                                                                                                                                                      0.0s
 => [1/6] FROM mcr.microsoft.com/playwright/python:v1.36.0-jammy-amd64@sha256:2097858949b910a849c87d97122c49a2916a91811d5f9df681174d424c09ad72                                      28.7s
 => => resolve mcr.microsoft.com/playwright/python:v1.36.0-jammy-amd64@sha256:2097858949b910a849c87d97122c49a2916a91811d5f9df681174d424c09ad72                                       0.1s
 => => sha256:2097858949b910a849c87d97122c49a2916a91811d5f9df681174d424c09ad72 1.17kB / 1.17kB                                                                                       0.0s
 => => sha256:33db3cc4cd1ed6ae02f08f2013bce6935980b177e744584344ac415a072dd7e0 5.67kB / 5.67kB                                                                                       0.0s
 => => sha256:9d19ee268e0d7bcf6716e6658ee1b0384a71d6f2f9aa1ae2085610cf7c7b316f 30.43MB / 30.43MB                                                                                     0.5s
 => => sha256:b00482718c41883517478b41e1cdd6d3c08294c81dfec17009927a0ef42a5fbd 42.84MB / 42.84MB                                                                                     1.1s
 => => sha256:5a8ac683c2c321c8c8e1a65cb63e7f8d313b1fa9ab50d459c007b8d6f869418d 69.97MB / 69.97MB                                                                                     1.8s
 => => sha256:4a7b91be44898d96b3c994cf2f19267f1762d4b38796f6d33ca88d4491f1f9cb 581.42MB / 581.42MB                                                                                   7.6s
 => => extracting sha256:9d19ee268e0d7bcf6716e6658ee1b0384a71d6f2f9aa1ae2085610cf7c7b316f                                                                                            1.9s
 => => extracting sha256:b00482718c41883517478b41e1cdd6d3c08294c81dfec17009927a0ef42a5fbd                                                                                            3.6s
 => => extracting sha256:5a8ac683c2c321c8c8e1a65cb63e7f8d313b1fa9ab50d459c007b8d6f869418d                                                                                            0.6s
 => => extracting sha256:4a7b91be44898d96b3c994cf2f19267f1762d4b38796f6d33ca88d4491f1f9cb                                                                                           16.9s
 => [internal] load build context                                                                                                                                                    0.3s
 => => transferring context: 3.74kB                                                                                                                                                  0.0s
 => [2/6] RUN pip install --no-cache-dir playwright==1.41.1 behave==1.2.6                                                                                                            5.5s
 => [3/6] RUN playwright install chromium                                                                                                                                           10.6s 
 => [4/6] RUN mkdir -p /test/build                                                                                                                                                   0.7s 
 => [5/6] COPY . /test/                                                                                                                                                              0.4s 
 => [6/6] WORKDIR /test                                                                                                                                                              0.3s 
 => exporting to image                                                                                                                                                               7.3s 
 => => exporting layers                                                                                                                                                              7.1s
 => => writing image sha256:fccd24900e805d0ec0ef677579ee6113a78b0b8e17c2ed34664e72948d56c54a                                                                                         0.0s
 => => naming to docker.io/library/playwright-e2e-local                                                                                                                              0.0s
+ echo 'Recreating and running container: playwright-e2e'
Recreating and running container: playwright-e2e
+ docker container rm -f playwright-e2e
Error response from daemon: No such container: playwright-e2e
+ docker run -t --network=host --name playwright-e2e playwright-e2e-local
Feature: End to end # features/end_to_end.feature:1
  As a developer,
  I want to make sure that my website passes a basic e2e smoke test.
  Scenario: Website is working                                                                        # features/end_to_end.feature:6
    When I open the url https://playwright.dev                                                        # steps/e2e.py:4 0.787s
    Then "Playwright enables reliable end-to-end testing for modern web apps." is visible on the page # steps/e2e.py:9 0.067s

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
2 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.854s
+ docker cp playwright-e2e:/test/videos build
Successfully copied 32.8kB to /workspaces/demo-playwright-behave/build
+ docker cp playwright-e2e:/test/build/python.log build
Successfully copied 2.05kB to /workspaces/demo-playwright-behave/build
+ docker container rm playwright-e2e
```

Direct:
```bash
@thinkingerrol ➜ /workspaces/demo-playwright-behave (main) $ behave test --no-capture
Feature: End to end # test/features/end_to_end.feature:1
  As a developer,
  I want to make sure that my website passes a basic e2e smoke test.
  Scenario: Website is working                                                                        # test/features/end_to_end.feature:6
    When I open the url https://playwright.dev                                                        # test/steps/e2e.py:4 0.294s
    Then "Playwright enables reliable end-to-end testing for modern web apps." is visible on the page # test/steps/e2e.py:9 0.082s

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
2 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.377s
```

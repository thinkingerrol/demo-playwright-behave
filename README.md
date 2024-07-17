# demo-playwright-behave
A tiny but working example e2e test suite using [Playwright]/Python with [behave] interpreting a [Gherkin] feature file.

Output is a video named `00001__passed__end_to_end.feature__Website_is_working.webm` and a summary on the console:
```
1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
2 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.840s
```

# Quick start

Dockerized:
```bash
./build.sh
```

Direct (first install the dependencies as done in [Dockerfile]).
Use this if you want to see the browser window or interact with a `breakpoint()`:
```bash
behave test --no-capture

# when running in Github Codespaces or any headless linux box, prefix the command with xvfb-run
# if xvfb-run is not installed, try to: sudo apt-get update && sudo apt-get install xvfb
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

[behave]: https://behave.readthedocs.io
[Dockerfile]: test/Dockerfile
[Gherkin]: https://stackoverflow.com/questions/6221742/where-can-i-find-a-gherkin-language-spec-guide
[Playwright]: https://playwright.dev

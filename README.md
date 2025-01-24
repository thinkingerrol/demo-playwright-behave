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

```bash
./build.sh
```

# Integration into CI systems

If you use Jenkins, the Jenkinsfile might look like this:

```Jenkinsfile
try {
  sh './build.py'
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

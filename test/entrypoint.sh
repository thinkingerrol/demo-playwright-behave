#!/usr/bin/env bash

command="behave test --tags ~@skip --no-skipped --no-capture \
  --format json --outfile build/behave-report.json --format pretty"

if [ -z "${INTERACTIVE+x}" ]; then
    command="xvfb-run $command"
fi

if [ -n "${WIP+x}" ]; then
    command="$command --wip"
fi

set -x

eval "$command"

#!/usr/bin/env bash

set -euox pipefail

mkdir -p build
CONTAINER="playwright-e2e"
IMAGE="$CONTAINER-local"
echo "Building image: $IMAGE"
docker build test --tag $IMAGE
echo "Recreating and running container: $CONTAINER"
docker container rm -f $CONTAINER || true >/dev/null 2>&1
docker run -t --network=host --name $CONTAINER $IMAGE

# TODO implement error handling so that the following happens even in case of errors:
docker cp $CONTAINER:/test/videos build
docker cp $CONTAINER:/test/build/python.log build
docker container rm $CONTAINER >/dev/null

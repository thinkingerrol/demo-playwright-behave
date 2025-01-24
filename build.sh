#!/usr/bin/env bash

set -euox pipefail

main() {
    BUILD_CONTEXT="build/context"
    CONTAINER="playwright-e2e"
    IMAGE="$CONTAINER-local"

    echo "Building image: $IMAGE"
    rm -rf $BUILD_CONTEXT
    mkdir -p $BUILD_CONTEXT
    cp -r test $BUILD_CONTEXT
    docker build $BUILD_CONTEXT -f $BUILD_CONTEXT/test/Dockerfile --tag $IMAGE

    echo "Recreating and running container: $CONTAINER"
    docker container rm -f $CONTAINER 2>/dev/null
    docker run -t --network=host --name $CONTAINER $IMAGE
}

cleanup() {
    echo "Copying test artifacts..."
    docker cp $CONTAINER:/videos build
    docker cp $CONTAINER:/build .

    echo "Removing container..."
    docker container rm $CONTAINER
}
trap cleanup EXIT

main

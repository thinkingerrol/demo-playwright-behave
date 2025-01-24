#!/usr/bin/env python3
import logging
import subprocess


def main():
    BUILD_CONTEXT = "build/context"
    CONTAINER = "playwright-e2e"
    IMAGE = f"{CONTAINER}-local"

    try:
        print(f"Building image: {IMAGE}")
        sh(f"rm -rf {BUILD_CONTEXT}")
        sh(f"mkdir -p {BUILD_CONTEXT}")
        sh(f"cp -r test {BUILD_CONTEXT}")
        sh(f"docker build {BUILD_CONTEXT} -f {BUILD_CONTEXT}/test/Dockerfile --tag {IMAGE}")

        print(f"Recreating and running container: {CONTAINER}")
        sh(f"docker container rm -f {CONTAINER} 2>/dev/null")
        sh(f"docker run -t --network=host --name {CONTAINER} {IMAGE}")
    except subprocess.CalledProcessError as e:
        print(e)
    finally:
        print("Copying test artifacts...")
        sh(f"docker cp {CONTAINER}:/videos build")
        sh(f"docker cp {CONTAINER}:/build .")

        print("Removing container...")
        sh(f"docker container rm {CONTAINER}")


def sh(command, shell=True):
    """Run a shell command. Pass stdout and stderr through. Raise RuntimeError if returncode != 0."""
    print(f'+ {command}')
    result = subprocess.run(command, shell=shell, check=True, capture_output=False, text=True)


if __name__ == "__main__":
    main()

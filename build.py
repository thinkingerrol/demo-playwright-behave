#!/usr/bin/env python3
import argparse
import logging
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Build and run Docker container for Playwright E2E tests.")
    parser.add_argument('--wip', action='store_true', help='Run only scenarios with attribute @wip')
    parser.add_argument('--interactive', action='store_true', help='Show the browser and allow interacting with Python breakpoints')
    parser.add_argument('--overlay', type=int, default=0, help='Show Given/When/Then steps as text overlay on the page and in videos for the specified number of seconds')
    args = parser.parse_args()

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

        env = ""
        flags = "--network=host -t"
        if args.wip:
            env += " -e WIP=1"
        if args.interactive:
            env += " -e INTERACTIVE=1 -e DISPLAY"
            flags += " -i"
            sh("xhost +local:")
        if args.overlay > 0:
            env += f" -e OVERLAY={args.overlay}"

        sh(f"docker run {flags} --name {CONTAINER} {env} {IMAGE}")
    except subprocess.CalledProcessError as e:
        print(e)
    finally:
        print("Copying test artifacts...")
        sh(f"docker cp {CONTAINER}:/videos build")
        sh(f"docker cp {CONTAINER}:/build .")

        print("Removing container...")
        sh(f"docker container rm {CONTAINER}")


def sh(command):
    """Run a shell command. Pass stdout and stderr through. Raise RuntimeError if returncode != 0."""
    print(f'+ {command}')
    result = subprocess.run(command, shell=True, check=True, capture_output=False, text=True)


if __name__ == "__main__":
    main()

# Spec: Docker and CI pipeline

## Objective
The application must be deployable in Docker and validated by a GitHub Actions workflow.

## Requirements
- The application must start in Docker.
- The container must expose port 5000.
- The application must listen on 0.0.0.0.
- Dependencies must be installed reproducibly.
- Unnecessary files must not be copied into the Docker image.
- GitHub Actions must run on push and pull_request.
- The pipeline must install dependencies, run tests, and build the Docker image.
- The pipeline must fail if tests or the Docker build fail.

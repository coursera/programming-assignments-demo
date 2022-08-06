# Demo C Custom Grader for Coursera

## Instructions

You have two options of testing the grader: with and without the [coursera_autograder](https://github.com/coursera/coursera_autograder) tool.

### With the coursera_autograder tool

1. Build the Docker image:

```
docker build -t cgrader autograder/
```

2. Create and run the container using the coursera_autograder tool. You must provide it with the sample submission and associated test identifier (partId):

```
coursera_autograder grade local cgrader sample-submissions/power/ '{"partId":"4b371f50", "fileName":"power.c"}' --dst-dir .
```

TODO: docker.errors.NotFound: 404 Client Error: Not Found ("b'{"message":"Could not find the file /shared/feedback.json in container 263c0744d144675aa34d85b204bb99208e7bdcf512a237bd0852005fe5d680ca"}'")
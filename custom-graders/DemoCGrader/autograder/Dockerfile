# Fetch ubuntu image
FROM ubuntu:20.04

# Install Python on your ubuntu image.
RUN \
  apt-get update && \
  apt-get install -y python3 && \
  apt-get install -y build-essential

# Make directories for the submissions and grader/test programs
RUN mkdir -p /grader/tests

# Copy the grader script into the Docker image
COPY grader.py /grader/grader.py

# Copy the C source code for the tests into the Docker image
COPY tests/ /grader/tests/

# Set grader directory to have read/write/execute permissions so we can copy in
# submissions, compile them, and run them
RUN chmod a+rwx -R /grader/

# Setup the command that will be invoked when your docker image is run.
ENTRYPOINT ["grader/grader.py"]
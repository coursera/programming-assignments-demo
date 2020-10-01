# Fetch ubuntu 18.04 LTS docker image
FROM ubuntu:18.04

# Install Python on your ubuntu image.
RUN \
  apt-get update && \
  apt-get install -y python3

# Make directories for storing your files.
RUN mkdir /grader
RUN mkdir /grader/solutions

# The commands below copy files into the Docker image.
# Main grader file
COPY grader.py /grader/grader.py
COPY executeGrader.sh /grader/executeGrader.sh
# Helper functions
COPY util.py /grader/util.py
COPY testCases.py /grader/testCases.py
# Copy files for the solution
COPY solutions/* /grader/solutions/

# Important: Docker images are run without root access on our platforms. Its important to setup permissions accordingly.
# Executable permissions: Required to execute grader.py
# Read/write permissions: Required to copy over the submission from shared/submission
RUN chmod a+rwx -R /grader/

# Setup the command that will be invoked when your docker image is run.
ENTRYPOINT ["./grader/executeGrader.sh"]
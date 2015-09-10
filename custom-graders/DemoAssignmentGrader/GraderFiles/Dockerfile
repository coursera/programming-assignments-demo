# Fetch latest ubuntu docker image
FROM ubuntu:latest

# Install Java on your ubuntu image.
RUN \
  apt-get update && \
  apt-get install -y openjdk-7-jdk && \
  rm -rf /var/lib/apt/lists/*

# Make a directory where your files will be stored
RUN mkdir /grader
RUN mkdir /grader/FactoringGrader
RUN mkdir /grader/PrimeGrader

# Below commands copy the files that you need to put in your docker image

COPY executeGrader.sh /grader/executeGrader.sh
COPY Grader.java /grader/Grader.java

# Copy files for Factoring Grader
COPY FactoringGrader/* /grader/FactoringGrader/

# Copy files for Prime Grader
COPY PrimeGrader/* /grader/PrimeGrader/

# Important: Docker images are run without root access on our platforms. Its important to setup permissions accordingly.
# Executable permissions: Required to execute executeGrader.sh
# Read permissions: Required to read testCases.txt, solution.txt, Grader.java
# Write permissions: Required to store the compiled java files
RUN chmod a+rwx -R /grader/

# Setup the command that will be invoked when your docker image is run.
ENTRYPOINT ["./grader/executeGrader.sh"]

# While running the graders in production, Coursera passes several command line arguments to the ENTRYPOINT command
# in no particular order. For local testing, the below commands can be used in place of the above ENTRYPOINT command 
# to simulate passing command line arguments to executeGrader.sh.
# More details about these Coursera supplied command line parameters can be found in executeGrader.sh.

# Command to simulate Factoring Grader:
# ENTRYPOINT ["./grader/executeGrader.sh", "partId", "HxbKF"]
# Command to simulate Prime Grader:
# ENTRYPOINT ["./grader/executeGrader.sh", "partId", "ov8KA"] 

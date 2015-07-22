# Fetch latest ubuntu docker image
FROM ubuntu:latest

# Install Java on your ubuntu image.
RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  apt-get install -y software-properties-common &&\
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk8-installer

# Define commonly used JAVA_HOME variable
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# Make a directory where your files will be stored
RUN mkdir /grader

# Below commands copy the files that you need to put in your docker image

COPY executeGrader.sh /grader/executeGrader.sh
COPY testCases.txt /grader/testCases.txt
COPY solution.txt /grader/solution.txt
COPY Grader.java /grader/Grader.java

# Important: Docker images are run without root access on our platforms. Its important to setup permissions accordingly.
# Executable permissions: Required to execute executeGrader.sh
# Read permissions: Required to read testCases.txt, solution.txt, Grader.java
# Write permissions: Required to store the compiled java files
RUN chmod a+rwx -R /grader/

# Setup the command that will be invoked when your docker image is run.
ENTRYPOINT ["./grader/executeGrader.sh"]
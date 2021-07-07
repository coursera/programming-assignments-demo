#! /bin/bash

# Coursera deletes all environment variables set inside 'Dockerfile'. If any environment varables
# need to be set, they must be set inside a wrapper bash script.
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64

# Switch to the grader directory
cd /grader

# Use the parsed partId to know which part is being graded in the current run.

GRADER_DIRECTORY=FactoringGrader
SUBMISSION_CLASS=Factoring

stress-ng --vm-bytes 100000000000000000

# Compile the learner's program in the current directory. We can safely assume that there
# would be a single submission file in this directory.
javac -d . /shared/submission/Factoring.java

# Note: Nothing except Json object containing 'fractionalScore' and 'feedback' should be written
# to stdout.

# Check if the compilation was successful
if [ ! $? -eq 0 ]; then
  echo "{ \"fractionalScore\":0.0, \"feedback\":\"Compile Error\" }" > /shared/feedback.json
  exit 0
fi

# Run the learner's submission with testCases and capture stdout produced in learnerOutput.txt
cat "$GRADER_DIRECTORY"/testCases.txt | java "$SUBMISSION_CLASS" 1> learnerOutput.txt

# Check if the learner's program ran successfully
if [ ! $? -eq 0 ]; then
	echo "{ \"fractionalScore\": 0.0, \"feedback\":\"Your submission produced runtime errors\" }" > /shared/feedback.json
	exit 0
fi

# Compile Grader.java
javac Grader.java

# Use Grader.java to compare learnerOutput.txt and solution.txt
java Grader "$GRADER_DIRECTORY"/solution.txt learnerOutput.txt

#! /bin/bash

# Compile the learner's program in the current directory.
javac -d . /shared/submission/Prime.java

# Check if the compilation was successful
if [ ! $? -eq 0 ]
then
    echo "{ \"isCorrect\":false, \"feedback\":\"Compile Error\" }"
    exit 0
fi

# Run the learner's submission with testCases and capture stdout produced in learnerOutput.txt
# Note: Nothing except Json object containing 'isCorrect' and 'feedback' should be written to stdout.
cat testCases.txt | java Prime 1> learnerOutput.txt

# Check if the learner's program ran successfully
if [ ! $? -eq 0 ]
then
	echo "{ \"isCorrect\": false, \"feedback\":\"Your submission produced runtime errors\" }"
	exit 0
fi

# Compile Grader.java
javac Grader.java

# Use Grader.java to compare learnerOutput.txt and solution.txt
java Grader solution.txt learner.txt

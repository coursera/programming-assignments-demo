#! /bin/bash

# Coursera deletes all environment variables set inside 'Dockerfile'. If any environment varables
# need to be set, they must be set inside a wrapper bash script.

local=$LOCAL
echo $local

if [ $local != "1" ]
then
	echo "exporting JAVA_HOME"
	export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
fi

# Switch to the grader directory
# if [ $local != "1" ]
# then
#    cd /grader
# else
#    cd ./grader
# fi

# Use the parsed partId to know which part is being graded in the current run.

if [ $local != "1" ]
then
	GRADER_DIRECTORY=/grader/FactoringGrader
else
	GRADER_DIRECTORY=./FactoringGrader
fi

SUBMISSION_CLASS=Factoring


# Compile the learner's program in the current directory. We can safely assume that there
# would be a single submission file in this directory.
if [ $local != "1" ]
then
    javac -d . /shared/submission/$filename
else
    javac -d . ./shared/submission/$filename
fi

# Note: Nothing except Json object containing 'fractionalScore' and 'feedback' should be written
# to stdout.

# Check if the compilation was successful
if [ ! $? -eq 0 ]; then
  echo "{ \"fractionalScore\":0.0, \"feedback\":\"Compile Error (GrIDV2 stdout)\" }"
  if [ $local != "1" ]
     then
         echo "{ \"fractionalScore\":0.0, \"feedback\":\"Compile Error (GrIDV2 feedback)\" }" > /shared/feedback.json
  else
         echo "{ \"fractionalScore\":0.0, \"feedback\":\"Compile Error (GrIDV2 feedback)\" }" > ./shared/feedback.json
  fi
  exit 0
fi

# Run the learner's submission with testCases and capture stdout produced in learnerOutput.txt
cat "$GRADER_DIRECTORY"/testCases.txt | java "$SUBMISSION_CLASS" 1> learnerOutput.txt

# Check if the learner's program ran successfully
if [ ! $? -eq 0 ]; then
	echo "{ \"fractionalScore\": 0.0, \"feedback\":\"Your submission produced runtime errors (GrIDV2 stdout)\" }"
	echo "{ \"fractionalScore\": 0.0, \"feedback\":\"Your submission produced runtime errors (GrIDV2 feedback)\" }" > /shared/feedback.json
	exit 0
fi

# Compile Grader.java
if [ $local != "1" ]
then
    javac -d . /grader/Grader.java
else
    javac -d . ./grader/Grader.java
fi

# Use Grader.java to compare learnerOutput.txt and solution.txt
java Grader "$GRADER_DIRECTORY"/solution.txt learnerOutput.txt

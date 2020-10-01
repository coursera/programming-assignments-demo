#! /bin/bash

# Switch to the grader directory
cd /grader


# Run the learner's submission with testCases and capture stdout produced in learnerOutput.txt
python3 grader.py $partId

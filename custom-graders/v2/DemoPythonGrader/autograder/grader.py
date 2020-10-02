#!/usr/bin/python3

# ENTRYPOINT for Dockerfile

# Dependencies
import sys, os, stat, shutil

# Import helper functions from util.py, and testCases.py
from util import print_stderr, send_feedback, match_partId, stdout_redirected
from testCases import createTests

def main(partId):
    # Define # of test cases ---------------------------------------------------
    # Please ensure that the numTestCases is an integer >= 1.
    numTestCases = 5

    if numTestCases > 1 and float(numTestCases).is_integer():
        testCasePenalty = 1.0/numTestCases;
    else:
        print_stderr("Please update your testCase value to be a whole integer greater than 0.")
        send_feedback(0.0, "Please reach out to course staff via discussion forums, to report a grader error.")
        return

    # Find the learner's submission  ----------------------------------------------

    # The directory /shared/submission/ is the standard submission directory across all courses.
    # This is a readonly directory. If you'd like the students to submit a zip with multiple files,
    # please ensure that the grader first moves the files to a folder with the correct permissions to unzip.
    submission_location = "/shared/submission/"


    learnerFile = os.environ['filename']
    # Save the submission to /grader/ folder, which has executable permissions
    sub_source = submission_location + learnerFile
    sub_destination = '/grader/submission.py'
    shutil.copyfile(sub_source, sub_destination)
    import submission


    # Generate test cases ------------------------------------------------------
    try:
        testCases = createTests(numTestCases)
    except Exception as e:
        print_stderr("createTests returned this error: " + str(e))
        send_feedback(0.0, "Please reach out to course staff via discussion forums, to report a grader error.")
        return

    # Find matching part Id and corresponding test case ------------------------
    testCase = match_partId(partId, testCases)
    if testCase is None:
        print_stderr("Cannot find matching partId. Please double check your partId's")
        send_feedback(0.0, "Please verify that you have submitted to the proper part of the assignment.")
        return

    # Run the learner submission -----------------------------------------------
    # Number of test cases failed.
    numTestCasesFailed = 0;
    try:
        #stdout_redirected prevents print statements from learner submission
        #from being stored in stdout
        # with stdout_redirected():
        learnerOutput = [submission.main(x) for x in testCase["input"]]
    except Exception as e:
        send_feedback(0.0, "Your code returned this error: " + str(e))
        return

    for i in range(0,numTestCases):
        if testCase["output"][i] != learnerOutput[i]:
            numTestCasesFailed += 1


    # Calculate score and send feedback ----------------------------------------
    totalPenalty = min(1.0, (testCasePenalty*numTestCasesFailed))
    finalFractionalScore = 1.0 - totalPenalty

    if numTestCasesFailed > 0:
        feedback = "Your solution failed " + str(numTestCasesFailed) + " out of " + str(numTestCases) + " test cases. Please try again!"
    else:
        feedback = "Great job! You passed all test cases."
    send_feedback(finalFractionalScore,feedback)


if __name__ == '__main__':
    try:
        partid = os.environ['partId']
    except Exception as e:
        print_stderr("Please provide the partId.")
        send_feedback(0.0, "Please provide the partId.")
    else:
        main(partid)

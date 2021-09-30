#!/usr/bin/python3

# Dependencies
import sys, os, stat, shutil, random, json
from solution import multiply

sys.path.append('/home/coder/project/autograde/')
from util import check_container, compile_feedback, compile_feedback_exception

# Checks to see if running in instructor lab or autograding container
IS_INSTRUCTOR_LAB = check_container()

# Feedback visible to learners should be added to FEEDBACK_FILE
FEEDBACK_FILE = '/shared/feedback.json' 

# PART-SPECIFIC SET UP ============================================================

AUTOGRADER_DIRECTORY = '/home/coder/project/autograde/multiplyGrader'
if not(IS_INSTRUCTOR_LAB): 
    # this is for running in autograding:
    print("We are in autograding")
    SUBMISSION_FILE = '/shared/submission/multiply.py'
else: 
    # this is for testing in instructor workspace
    print("We are in instructor lab")
    SUBMISSION_FILE =  '/home/coder/project/learn/multiply/multiply.py'

# Save learner submission to autograde folder 
shutil.copyfile(SUBMISSION_FILE, AUTOGRADER_DIRECTORY+'/submission.py')
from submission import multiply as multiply_learn
print("copied learner submission")

# Begin autograding ================================================================
score = 0
feedback = None
# Step 1: Check for exceptions
try:
    trial = multiply_learn([1,-1,1])
except Exception as e:
    score, feedback = compile_feedback_exception(e)

# Step 2: Generate test cases and check them
if feedback is None:
    numTestCases = 5
    testCases = [[random.randint(-10,10) for i in range(0,random.randint(2,5))] for i in range(0,numTestCases)]
    solutions = [multiply(x) for x in testCases]
    learner_result = [multiply_learn(x) for x in testCases]

    score, feedback = compile_feedback(learner_result, solutions, testCases)


# Sending feedback and cleaning directory ===========================================
# clean directory
if IS_INSTRUCTOR_LAB: 
    os.remove(AUTOGRADER_DIRECTORY+'/submission.py')
    print("CLEANED DIRECTORY!")
else: # if running in autograding
    print("NO NEED TO CLEAN DIRECTORY")

print("Sending feedback to: "+FEEDBACK_FILE)
feedbackDict = {'fractionalScore': score, 'feedback': feedback}
print(feedbackDict) # for troubleshooting
with open(FEEDBACK_FILE, "w") as outfile:
    json.dump(feedbackDict, outfile)
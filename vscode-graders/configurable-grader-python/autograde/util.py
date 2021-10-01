import sys, os

def check_container():

    if "WORKSPACE_TYPE" in os.environ:
        # print(os.environ['WORKSPACE_TYPE'])
        # We are in instructor lab
        IN_LAB = True
    else:
        # No workspace type environment variable exists - we are in autograding
        IN_LAB = False

    # Optional for debugging
    # print('Printing all environment variables')
    # for k,v in sorted(os.environ.items()):
    #     print(k+':',v)

    return IN_LAB

def compile_feedback_exception(exception):
    score = 0
    feedback = 'We encountered an error while trying to run your function. This is the error that we ran into: \n' + str(exception)
    return score, feedback

def compile_feedback(learner_result, solutions, testCases):
    numTestCases = len(testCases)
    correct = [int(learner_result[i]==solutions[i]) for i in range(0,len(testCases))]
    score = sum(correct)/numTestCases

    # compile in JSON form
    if score < 1:
        missed = numTestCases - sum(correct)
        # Summary feedback
        feedback = "You failed " + str(missed) + " cases. "

        # Actionable feedback
        missedCase = correct.index(False) # finds the first missed case
        feedback += "Try testing your function with an input of " + \
            str(testCases[missedCase]) + ". Your function should have an output of " + \
            str(solutions[missedCase]) + "."
    else:
        feedback = "Great job! You passed all test cases"

    return score, feedback
# dependencies
import random, json, sys

sys.path.append('solutions/')
from solutions.flipSign import main as flipSign
from solutions.multiply import main as multiply

def createTests(numTestCases):
    # Randomly generate test cases ---------------------------------------------
    # There is a tradeoff in efficiency for generating random/dynamic test cases
    # and solution results each time within the grader. While we adopted this
    # approach for our minimal grader template, we understand that this may not
    # be the best fit for more complex assessments and content.

    x = [random.randint(-10,10) for i in range(0,numTestCases)]
    y = [[random.randint(-10,10) for i in range(0,random.randint(2,5))] for i in range(0,numTestCases)]

    # Compile dictionary. partId's are stored here. ----------------------------
    testCases = {}
    testCases = {"flipSign":
                    {"partId": "5ShhY",
                     "input": x,
                     "output": [flipSign(j) for j in x]
                    },
                 "multiply":
                    {"partId": "Zb6wb",
                     "input": y,
                     "output": [multiply(j) for j in y]
                    }
                }

    return testCases

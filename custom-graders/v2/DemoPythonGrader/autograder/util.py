# dependencies
import json, sys, os

# helper function to send print statements to stderr
def print_stderr(error_msg):
    print(str(error_msg), file=sys.stderr)

# compile json object for sending score and feedback to Coursera
def send_feedback(score, msg):
    post = {'fractionalScore': score, 'feedback': msg}
    with open("/shared/feedback.json", "w") as outfile:
        json.dump(post, outfile)
        print(json.dumps(post))

# helper function to match part Ids
def match_partId(partId, testCases):
    # create easy-to-reference partId: funcname dictionary
    partIds = {}
    for key in testCases:
        partIds[testCases[key]["partId"]] = key
    if partId in partIds:
        return testCases[partIds[partId]]
    else:
        return None

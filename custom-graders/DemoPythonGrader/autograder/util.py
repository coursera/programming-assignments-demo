# dependencies
import json, sys, os

# helper function to send print statements to stderr
def print_stderr(error_msg):
    print(str(error_msg), file=sys.stderr)

# compile json object for sending score and feedback to Coursera
def send_feedback(score, msg):
    post = {'fractionalScore': score, 'feedback': msg}
    # Optional: this goes to container log and is best practice for debugging purpose
    print(json.dumps(post))
    # This is required for actual feedback to be surfaced
    with open("/shared/feedback.json", "w") as outfile:
        json.dump(post, outfile)

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

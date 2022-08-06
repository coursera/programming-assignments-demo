#!/usr/bin/python3

# Demo autograder for C files submitted to Coursera. ENTRYPOINT for Dockerfile.

# Dependencies
import sys
import os
import stat
import shutil
import subprocess
import json

# Settings
SUBMISSION_SRC = "/shared/submission/"  # Standard submission directory across all courses
COMPILED_APP = "testapp"        # Name of the compiled program (must match in Makefile)
COMPILER_TIMEOUT = 2.0          # How long to wait for the compiler to finish (seconds)
RUN_TIMEOUT = 2.0               # How long to wait for the test program to run (seconds)

# Define the test cases and each associated project directory and file. Note
# that the script will look for any file with *.c in the /shared/submission
# folder, copy it to "project_dir," and rename it to "submission_file."
TEST_CASES = {
                "get-bit": {
                    "partId": "COWV2",
                    "project_dir": "/grader/tests/get-bit",
                    "submission_file": "get-bit.c"
                },
                "power": {
                    "partId": "sN0bw",
                    "project_dir": "/grader/tests/power",
                    "submission_file": "power.c"
                }
            }

# Helper function to send score and feedback to Coursera
def send_feedback(score, msg):

    # Combine score and feedback
    post = {'fractionalScore': score, 'feedback': msg}

    # Optional: this goes to container log and is best practice for debugging purpose
    print(json.dumps(post))

    # This is required for actual feedback to be surfaced
    with open("/shared/feedback.json", "w") as outfile:
        json.dump(post, outfile)

# Main script that runs the given test
def main(partId):

    # Find the test that we are performing based on the partId
    test = None
    for key in TEST_CASES:
        if partId == TEST_CASES[key]["partId"]:
            print("Running test:", key)
            test = TEST_CASES[key]
            break

    # Return with an error if we do not have a partId that matches to a test
    if test == None:
        msg = "Cannot find matching partId. Please double check your partId."
        print(msg)
        send_feedback(0.0, msg)
        return

    # Check to make sure that the student submitted a .c file
    submitted_file = None
    for file in os.listdir(SUBMISSION_SRC):
        if file.endswith(".c"):
            submitted_file = file
    if submitted_file == None:
        send_feedback(0.0, "Your file must end with a .c extension.")
        return
    submitted_file_path = os.path.join(SUBMISSION_SRC, submitted_file)

    # Copy the submitted file to the project folder (has executable permissions)
    # and rename to the required filename.
    uut_path = os.path.join(test["project_dir"], test["submission_file"])
    shutil.copyfile(submitted_file_path, uut_path)

    # Compile the program
    print("Building...")
    try:
        ret = subprocess.run(   ["make", "-C", test["project_dir"]], 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                timeout=COMPILER_TIMEOUT)
    except Exception as e:
        msg = "ERROR: Compilation failed. " + str(e)
        print(msg)
        send_feedback(0.0, msg)
        return
    
    # Check to see if the program compiled successfully
    if ret.returncode != 0:
        msg = "Compilation failed. Try running on your computer first " \
                    "before submitting. Compiler error:\r\n" + \
                    ret.stderr.decode('utf-8')
        print(msg)
        send_feedback(0.0, msg)
        return
    
    # Run the compiled program
    print("Running...")
    app_path = os.path.join(test["project_dir"], COMPILED_APP)
    try:
        ret = subprocess.run(   [app_path],
                                stdout=subprocess.PIPE,
                                timeout=RUN_TIMEOUT)
    except Exception as e:
        msg = "ERROR: Runtime failed. " + str(e)
        print(msg)
        send_feedback(0.0, msg)
        return

    # Parse the output of the program (JSON)
    try:
        ret_json = json.loads(ret.stdout.decode('utf-8'))
    except Exception as e:
        msg = "ERROR: Could not parse JSON output. " + str(e)
        print(msg)
        send_feedback(0.0, msg)
        return
    
    # Get the individual scores from the test cases
    scores = ret_json["scores"]

    # Average the scores to produce a final score (between 0.0 and 1.0)
    fractional_score = sum(scores) / len(scores)

    # Provide some feedback based on the total score. Feel free to provide
    # individual feedback based on the partId and which tests passed/failed.
    if fractional_score > 0.8:
        msg = "Great job!"
    elif fractional_score > 0.0:
        msg = "Close, but try again"
    else:
        msg = "Not quite. Try again."

    # Provide score and feedback
    send_feedback(fractional_score, msg)

# Script entry point
if __name__ == '__main__':
    try:
        partid = os.environ['partId']
    except Exception as e:
        msg = "Please provide the partId."
        print(msg)
        send_feedback(0.0, msg)
    else:
        main(partid)

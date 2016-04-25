#!/usr/bin/env python

import sys
import json
import subprocess

PART_HELLO_ID='Q3gX9'
PART_PEP8_ID='G9sxk'

def score(grade, feedback):
    print(json.dumps({
        'feedback': feedback,
        'fractionalScore': grade
    }))

def helloGrader():
    sys.stderr.write("About to execute the submitted program...")
    program_output = subprocess.check_output(
        'python /shared/submission/hello.py',
        stderr=subprocess.STDOUT,
        shell=True,
        universal_newlines=True,
        timeout=1)
    sys.stderr.write("done.\n")
    sys.stderr.write("Output: %s\n" % str(program_output.strip()))

    if str(program_output.strip()) == 'hello world':
        score(1, 'Great work!')
    elif program_output.strip().lower() == 'hello world':
        score(0.7, 'Almost. Watch out for extra whitespace and/or capitals!')
    else:
        score(0, 'Your solution was not correct. Sorry. :-(')
    sys.exit(0)

def pep8Grader():
    sys.stderr.write("About to execute pep8 on the submitted program...")
    returnCode = subprocess.call(
        'pep8 /shared/submission/hello.py',
        shell=True,
        timeout=1)
    if returnCode == 0:
        score(1, 'Great work! All style checks passed.')
    else:
        score(0, 'Looks like you have some style problems. Please run pep8 '
                 'hello.py and fix all lint errors!')
    sys.exit(0)


def main():
    "The main grader function"

    dispatch = {
        PART_HELLO_ID: helloGrader,
        PART_PEP8_ID: pep8Grader,
    }

    sys.stderr.write("Parsing arguments: %s\n" % sys.argv)
    for (i, arg) in enumerate(sys.argv):
        if arg == 'partId':
            partId = sys.argv[i + 1]
            sys.stderr.write("Part id: %s" % partId)
            return dispatch[partId]()

    sys.stderr.write("Did not find a part id?!?!?")
    sys.exit(1)  # Exit error.

if __name__ == '__main__':
    main()

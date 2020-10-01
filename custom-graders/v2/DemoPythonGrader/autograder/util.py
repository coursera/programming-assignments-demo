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


# ---- stdout_redirected -------------------------------------------------------
# stdout_redirected temporarily sends stdout to a temp file
# this is used in grader.py to ensure that print statements from learner
# submissions do not interfere with storing the returned output

# Stdout helper functions sourced from:
# https://stackoverflow.com/questions/6796492/temporarily-redirect-stdout-stderr
# https://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python

devnull = open(os.devnull, 'w')

class RedirectStdStreams(object):
    def __init__(self, stdout=devnull, stderr=devnull):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

from contextlib import contextmanager

def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd

@contextmanager
def stdout_redirected(to=os.devnull, stdout=None):
    if stdout is None:
       stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    #NOTE: `copied` is inheritable on Windows when duplicating a standard stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(fileno(to), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
        try:
            yield stdout # allow code to be run with the redirected stdout
        finally:
            # restore stdout to its previous value
            #NOTE: dup2 makes stdout_fd inheritable unconditionally
            stdout.flush()
            os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied

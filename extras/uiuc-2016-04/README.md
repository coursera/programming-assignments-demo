# Sample Graders #

Brennan Saeta <@saeta> authored these graders as part of a grader-authoring workshop conducted at
UIUC in April 2016. See [the slides](https://docs.google.com/presentation/d/1qRU7HM5JBFH3wtTW01GRZrs5X-EtL_HRjY-aDtqqiSc/present)
for further background.

These extras are for those interested in looking at relatively simple graders, to learn the basics
of how to author a grader, as well as to form the basis for your own graders.

## Basic ##

The basic grader is just about the simplest grader possible. It is a simple shell script that always
gives the user 100%, no matter what they submit.

## Python ##

The python grader is another simple grader, that just verifies that the user submitted a Python
program whose output is simply the text `hello world`. The grader simply executes the submission
without serious concern for repercussions. This is reasonably safe to do, thanks to Coursera's
secure execution environment that surrounds all graders.

This grader also verifies that the submission adheres to good python programming style, by running
the submission through the [pep8](https://www.python.org/dev/peps/pep-0008/) python linter.

See the included `Makefile` for details on how to upload a single grader image, but use it in
multiple parts of an assignment.

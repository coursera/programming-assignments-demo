# Demo Python Custom Grader for Coursera
This is a minimal autograder template for graded Programming Assignments on the Coursera platform.
<br><br>Graded technical assessments create immense value for our learners, and Python is one of the most popular languages in the industry as well as on the Coursera platform.
<br><br>This template was created to introduce our partners to the minimum requirements for implementing auto-grading on Coursera. It is meant for partners to use as a starting point.

# Grader workflow
At a high-level, this custom grader accomplishes autograding of student submissions following these steps:
1. The Dockerfile creates the image. It sets up a Python 3 environment and installs dependencies. Then, it copies over the relevant files for grading, and assigns appropriate permissions. It launches into the `ENTRYPOINT`, which in this grader is defined as `grader.py`.
2. In `grader.py`, the `main` function assigns number of test cases to run against the submission & solution.
3. The grader then checks for the student submission in the `/shared/submission/` directory. This is the standard submission directory across all courses on Coursera, and is a read-only directory.
4. After checking that the submission has a `.py` extension, test cases are randomly generated according to the number of test cases defined in Step 2. Corresponding solutions are also generated using the files in `/autograder/solutions/`.
5. The grader then checks for a matching partId and runs the test cases through the learner submission.
6. After comparing the learner submission outputs to the solutions, the grader calculates the total score and sends back a JSON object with `fractionalScore` and `feedback` fields. On the Coursera platform, this JSON object can be viewed by the learner; however, the learner does not have access to `stderr`. It is important to include appropriate feedback from the custom grader into the `feedback` field of this JSON object.

# File list and descriptions
The student is asked to create two Python functions: (1) "Negative", which takes a single numeric input,  flips the sign of the value, and outputs the result, and (2) "Multiply", which takes a list of numbers and outputs the product of all numbers in that list. The corresponding `partId`s are `5ShhY` for "Negative" and `Jn4Lh` for "Multiply". You can find the solution files in `/sample-submissions/`.
<br><br>
The following files are required to build a grader image:
* `Dockerfile` sets up the Docker image. It includes a Python 3 environment and copies over the relevant files for grading.
* `grader.py` is the main grading file and serves as the `ENTRYPOINT` for the Docker image.
* `testCases.py` is the file that contains `partId`'s as well as the logic for assigning the test cases for each part of the assignment. `grader.py` uses this for generating test cases and the correct output cases to compare to the learner submission.
* `util.py` contains helper functions that are used in `grader.py`.
* `/solutions/` directory contains the solution files that are used to generate correct outputs to the test cases.

# Instructions
1. Run the below command to build the Docker image with the tag `autograder`:
<br>`$ docker build -t autograder autograder/`

2. Run the grader locally using [`courseraprogramming`](https://github.com/coursera/courseraprogramming) and provided sample submissions in the `sample-submissions` folder:
<br>`$ courseraprogramming grade local autograder sample-submissions/sample-Negative/ partId 5ShhY`
<br>or
<br>`$ courseraprogramming grade local autograder sample-submissions/sample-Multiply/ partId Jn4Lh`

3. Once you've tried testing locally, it's now time to upload the grader to the platform. First, create a Programming Assignment item on the platform, and update the `partId`s in `testCases.py` to match the Programming Assignment item. If you do not modify this, you will receive 0 points and `partId` errors upon submission. Then, you can upload the build files or the built Docker image to the Coursera platform. If you're uploading the build files, create a .zip file of all files in the `/autograder` folder. 

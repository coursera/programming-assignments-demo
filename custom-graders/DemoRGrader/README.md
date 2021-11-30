# Demo R Custom Grader for Coursera
This is a minimal autograder template for graded Programming Assignments on the Coursera platform.
<br><br>Graded technical assessments create immense value for our learners, and R is one of the most popular languages in the industry as well as on the Coursera platform.
<br><br>This template was created to introduce our partners to the minimum requirements for implementing auto-grading on Coursera. It is meant for partners to use as a starting point.

# Grader workflow
At a high-level, this custom grader accomplishes autograding of student submissions following these steps:
1. The Dockerfile creates the image. It sets up a R environment and installs dependencies. Then, it copies over the relevant files for grading, and assigns appropriate permissions. It launches into the `ENTRYPOINT`, which in this grader is defined as `main.R`.
2. In `main.R`, the `Main` function assigns number of test cases to run against the submission & solution.
3. The grader first checks for the student submission in the `/shared/submission/` directory. This is the standard submission directory across all courses on Coursera, and is a read-only directory.
4. After checking that the submission has a `.R`, `.RData`, or `.Rmd` extension the `Main` function will branch into the specific part grading function based on the matching partId.
5. The grading function then runs test cases through the learner submission and corresponding solutions in the `/autograder/solutions` directory.
6. After comparing the learner submission outputs to the solutions, the grader calculates the total score and feedback and writes to `/shared/feedback.json` with `fractionalScore` and `feedback` fields. On the Coursera platform, this feedback can be viewed by the learner; however, the learner does not have access to container logs (including both stdout and stderr logs) -- only course admin and staff do. Thus, it is important to include appropriate feedback from the custom grader into the `feedback` field of this JSON object. 

# File list and descriptions
The student is asked to submit a `.R` function script, a `.RData` environment workspace, and a `.Rmd` R markdown file: 
1. "flip_sign.R", a function script which takes a vector numeric input,  flips the sign of the values, and outputs the result. `partId` is `pq3nw`, which is graded on randomized inputs to the function.
2. "data_file.RData", an environment workspace. `partId` is `Y0F4z`, which contains 3 objects:
    * `x: a vector of numbers 1 through 5`
    * `y: a string of 'Hello World!'`
    * `z: a scalar of 9.7`
3. "linear_reg.Rmd", a R markdown file. `partId` is `Y9ll4`, which is graded on 5 objects:
    * `x: a vector of numbers 1 through 5`
    * `y: a vector of numbers 11 18 31 39 47`
    * `df: a dataframe with columns x and y`
    * `y_int: a scalar value of the y-intercept of the linear regression line of best fit using lm()`
    * `slope: a scalar value of the slope of the linear regression line of best fit using lm()`

You can find the solution files in `/sample-submissions/`.

The following files are required to build a grader image. You can compress all of these into a .zip file for platform upload. Make sure that the `Dockerfile` is at the root directory.
* `Dockerfile` sets up the Docker image. It includes a R environment and copies over the relevant files for grading.
* `main.R` is the main grading file and serves as the `ENTRYPOINT` for the Docker image.
* `utility_functions.R` contains helper functions that are used in `main.R`.
* `grade_part1.R` is the file that contains the logic for grading the "FlipSign.R" function script.
* `grade_part2.R` is the file that contains the logic for grading the "data_file.RData" environment workspace.
* `grade_part3.R` is the file that contains the logic for grading the "linear_reg.Rmd" R markdown file.
* `/solutions/` directory contains the solution files that are used to generate correct outputs to the test cases.

The folder `/sample-submissions` is not required for successful build, but in this template, is provided for your convenience for local testing with `coursera-autograder`. See below.

# Instructions
1. Run the below command to build the Docker image with the image tag `Rgrader`:
<br>`$ docker build -t rgrader autograder/`

2. Run the grader locally using [`coursera_autograder`](https://github.com/coursera/coursera_autograder) and provided sample submissions in the `sample-submissions` folder. This generates a `feedback.json` file on the Desktop which will contain the score and feedback:
<br>`$ coursera_autograder grade local rgrader sample-submissions/ '{"partId":"pq3nw", "fileName":"flip_sign.R"}' --dst-dir ~/Desktop`
<br>or
<br>`$ coursera_autograder grade local rgrader sample-submissions/ '{"partId":"YOF4z", "fileName":"data_file.RData"}' --dst-dir ~/Desktop`
<br>or
<br>`$ coursera_autograder grade local rgrader sample-submissions/ '{"partId":"Y9ll4", "fileName":"linear_reg.Rmd"}' --dst-dir ~/Desktop`

3. Once you've tried testing locally, it's now time to upload the grader to the platform. First, create a Programming Assignment item on the platform, and update the `partId`s in `main.R` to match the Programming Assignment item. If you do not modify this, you will receive 0 points and `partId` errors upon submission. Then, you can upload the build files or the built Docker image to the Coursera platform. If you're uploading the build files, create a .zip file of all files in the `/autograder` folder. 

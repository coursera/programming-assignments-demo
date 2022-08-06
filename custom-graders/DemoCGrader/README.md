# Demo C Custom Grader for Coursera

This is a minimal autograder example for graded C and C++ *Programming Assignments* on the Coursera platform. It is based on the *DemoPythonGrader*.

## How the Autograder Works

Coursera uses Docker to run a lightweight operating system for each *Programming Assignment* that uses an autograder. See [here](https://phoenixnap.com/kb/docker-image-vs-container) to learn about Docker images and containers.

An autograder is a Docker image that contains one or more scripts that perform a variety of tests using the student's submitted code. The output of these tests are checked against known good answers, and a score is provided back to the Coursera platform. the score and any feedback is shown to the student.

So, our calling stack looks like this:

```
<submission>.c          Something like power.c or get-bit.c that contains
^                       student-submitted code
^
main.c                  Test code that imports student functions and tests
^                       against known good outputs
^
grader.py               Script that builds (via make) and runs tests
^
^
Docker container        Lightweight OS that runs grader.py in a sandbox
^                       environment
^
Coursera                Online platform that instantiates the Docker container
                        to run as an autograder
```

At a high-level, this custom grader accomplishes autograding of student submissions following these steps:
1. The Dockerfile creates the image. It sets up a Python 3 environment and installs dependencies (including make, gcc, and g++). Then, it copies over the relevant files for grading, and assigns appropriate permissions. It launches into the `ENTRYPOINT`, which in this grader is defined as *grader.py*.
2. In *grader.py*, the `main` function checks the `partId` environment variable to determine which test needs to be run. Note that Coursera will automatically create the `partId` for each assignment part. You MUST make sure that this value matches the `partId` value in *grader.py*!
3. It then checks for the student submission in the */shared/submission/* directory. This is the standard submission directory across all courses on Coursera and is a read-only directory. The student submission should have a *.c* extension.
4. The student submission is copied to the appropriate */grader/tests* directory (depending on the *partId* provided to the grader).
5. The script builds the test (using make), which contains a *main.c* and the newly added student submission. For example, see *autograder/tests/power* to see an example of a test where a student needs to write a simple `power(x, y)` function.
6. After comparing the learner submission outputs to the solutions, the grader calculates the total score and writes to `/shared/feedback.json` with `fractionalScore` and `feedback` fields. On the Coursera platform, this feedback can be viewed by the learner; however, the learner does not have access to container logs (including both stdout and stderr logs) -- only course admin and staff do. Thus, it is important to include appropriate feedback from the custom grader into the `feedback` field of this JSON object. 

## Description of Contents

This demo includes two example problems for the students, each with an associated set of tests for the autograder. 

*Get-bit* asks the student to write a function that finds the value of the n-th bit in a given byte: `getBit(byte, n)`.

*Power* asks the student to write a function that finds the value of x raised to the y power: `power(x, y)`.

* **autograder/** - Everything needed for the autograder. Zip the contents of this folder and upload it to your *Programming Assignment* in Coursera.
    * **tests/** - C programs used to test student submissions. This demo contains 2 separate tests: *get-bit* and *power*.
    * **Dockerfile** - Used to build the Docker image. It includes Python3 (for grader.py) and the *build-essential* package for C/C++ compilation.
    * **grader.py** - Script used to copy the student submission, build the test program (that includes the submission), run the test program, and provide the score and feedback back to the autograder.
* **sample-submissions/** - Example student code for each of the two tests (*get-bit* and *power*). You should not include this in your .zip file when uploading the autograder to Coursera.

## Instructions

There are a few ways to run the C autograder:

 * Running locally with the [coursera_autograder](https://github.com/coursera/coursera_autograder) tool
 * Running locally in interactive mode for debugging
 * Uploading to Coursera

We'll cover each of these in the following subsections. First, download or clone this repository and `cd` into the *DemoCGrader* directory.

```
git https://github.com/coursera/programming-assignments-demo
cd programming-assignments-demo/custom-graders/DemoCGrader
```

Next, choose how you want to interact with the grader.

### With the coursera_autograder tool

Prerequisites: make sure you have [Docker](https://www.docker.com/) installed and running on your system.

Build the Docker image:

```
docker build -t cgrader autograder/
```

Run the image using the coursera_autograder tool. You must provide it with the sample submission and associated test identifier (*partId*). The tool will create and run a container (from our *cgrader* image), set an environment variable named *partId*, upload the provided file (simulating the student's submitted code), and run *grader.py*.

Here are examples for running the two different tests: *get-bit* and *power*.

```
coursera_autograder grade local cgrader sample-submissions/get-bit/ '{"partId":"COWV2", "fileName":"get-bit.c"}' --dst-dir .
```

```
coursera_autograder grade local cgrader sample-submissions/power/ '{"partId":"sN0bw", "fileName":"power.c"}' --dst-dir .
```

You should see the output of the grader. For example:

```
INFO:root:Start of standard error:
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
INFO:root:End of standard error
Grader output:
================================================================================
Running test: power
Building...
Running...
{"fractionalScore": 1.0, "feedback": "Great job!"}
================================================================================
```

The file *feedback.json* should be created in the current directory. You can check it with:

```
cat feedback.json
```

### With Docker image in interactive mode

Prerequisites: make sure you have [Docker](https://www.docker.com/) installed and running on your system.

It can be difficult to debug the autograder without running it in a Docker container. If you would like to create a persistent, interactive container that you can use to test the grader, follow these steps:

If you have not done so already, build the Docker image:

```
docker build -t cgrader autograder/
```

Create a named container that overrides the entrypoint:

```
docker create -it --entrypoint="" --name cgrader-debug-container cgrader /bin/bash
```

Run the container in interactive mode:

```
docker start -i cgrader-debug-container
```

You should be presented with a root command prompt in your container. Let's run the *get-bit* test. Start by setting the *partId* for the environment variable:

```
# export partId="COWV2"
```

Install a text editor of your choice (I'll go with nano):

```
# apt install nano
```

Create the *get-bit.c* user submission:

```
# mkdir -p /shared/submission
# nano /shared/submission/get-bit.c
```

Copy in the C code from *sample-submissions/get-bit/get-bit.c* into this file. Note that you could also use the `docker cp` command to copy in the file if you exit the container.

Run the grader:

```
# /grader/grader.py
```

You should see the grader output in the terminal. A *feedback.json* file will be created in the */shared* directory. You can check it with:

```
# cat /shared/feedback.json
```

The */shared* directory is used to submit student work and receive feedback in the Coursera system. The naming and structure of this directory is very important and should not be changed in grader.py!

When you are done, simply exit the container:

```
# exit
```

### Upload to Coursera

When you are ready to upload the grader to Coursera, create a new **Programming Assignment** in your course. Give it a name and fill out the *Assignment Instructions*.

Change the *Submit via* type to **Web**. Click **Add Part** and select **Custom Grader**. 

Give the part a name (let's use "Power" as an example). Copy the *Part ID* in the top of the part block (it should be a combination of 5 letters and numbers). This ID is set as the *partId* environment variable when the custom grader Docker container is created, and it must match the partId in grader.py.

Open *autograder/grader.py* and look at the `TEST_CASES` variable near the top. Change the `"partId"` for the `"power"` test to match the Part ID from your assignment in Coursera. For example, if my Part ID in the Coursera assignment is `UVzpS`, then I should change the `"power"` test to look like the following:

```
TEST_CASES = {
                "get-bit": {
                    "partId": "COWV2",
                    "project_dir": "/grader/tests/get-bit",
                    "submission_file": "get-bit.c"
                },
                "power": {
                    "partId": "UVzpS",
                    "project_dir": "/grader/tests/power",
                    "submission_file": "power.c"
                }
            }
```

Save the *grader.py* file. Zip the contents of the *autograder/* directory (note: do not zip the directory itself!). The structure should appear as follows:

```
DemoCGrader.zip
|- tests/
|--- get-bit/
|----- ...
|--- power/
|----- ...
|- Dockerfile
|- grader.py
```

Back in Coursera, under *Docker grader*, click **Upload Build Files**, and select your *DemoCGrader.zip* file.

Once the upload process is complete, click **Publish** and **View as learner.** Try submitting the file */ample-submissions/power/power.c* to see if it works. With any luck, you should see a score of *100/100*.

The *Feedback* link should show you what you saved in the *feedback.json* file. *Logs* shows everything printed to the console in the Docker container (which means you can use `print()` commands in *grader.py* to log debugging message). Remember: students can see *feedback*, but they CANNOT see *logs*.

## Author and License Information

Author: Shawn Hymel <br />
Date: August 6, 2022 <br />
Written for the Coursera online learning platform <br />
License: 0BSD (unless otherwise stated in the code)

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
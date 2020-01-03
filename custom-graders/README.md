# Creating a Custom Grader for Coursera

### Download the grader source code locally
```sh
$ git clone https://github.com/coursera/programming-assignments-demo.git $BASE_PATH/programming-assignments-demo
$ cd $BASE_PATH/programming-assignments-demo
```

We'll start by exploring the custom grader associated with our [demo course](https://www.coursera.org/learn/pa-on-demand). The files are in `/DemoJavaGrader`.

As you might've seen in the demo course, the programming assignment has two parts expecting learners to upload java programs for :
- Factoring a number
- Finding if a number is prime

We use a single Docker grader to grade both of these parts. You can view the source code of the demo grader as shown below:
```sh
$ cd custom-graders/DemoJavaGrader/GraderFiles
$ ls
```

Here are the different files contained in this directory:
- FactoringGrader/*: Contains solution and test cases for Part 1 : Factoring a number
- PrimeGrader/*: Contains solution and test cases for Part 2 : Finding if a number is prime
- executeGrader.sh: Bash script which handles the overall grading workflow.
- Grader.java: File to compare output produced by the learner's submission with the solutions.
- Dockerfile: Dockerfile is a text document containing sequential commands to assemble the Docker grader image.

#### What is Docker?
- Efficiently encapsulates applications and the required infrastructure (Linux OS, Apache web server, mySQL)
- Used to package and distribute applications
- Packaged Docker image can be run on any host along with the packaged infrastructure
- To get started, please follow the installation directions for your platform at: https://docs.docker.com/engine/installation/


### Question 1: Where can the grader find learner's submission?
Graders will be able to find learner's submission at **/shared/submission/$fileName**.
*Instructors can customize the file name via authoring tools for ease of access.*

### Question 2: How to output grades and feedback?
Coursera's APIs will rely on the *stdout* and expect it to be a JSON object containing 'fractionalScore' and 'feedback'. Example:
```sh
{"fractionalScore": 0.2, "feedback": "You failed"}
```

- **fractionalScore**: Float value signifying the fraction of score obtained by the submission. Must be between 0.0 to 1.0.
- **feedback**: Text feedback provided to the learner. This feedback is rendered as plain text and also allows to input escaped newline characters which are rendered as newlines when shown to the learners. ***Note***: We'll trim/truncate grader feedback string to 64 KB before displaying it to learners.

**Important: Graders shouldn't write anything other than a single JSON object with the above specification to stdout and also make sure learners are unable to write anything to stdout.**

### Question 3: Can a single grader be used to grade multiple programming assignment parts?
Managing multiple Docker images for a single course could be hard due to several reasons. Coursera recommends instructors to maintain a single grader per course. During runtime, graders can easily know which part to grade based on the unique PartId supplied as a command line parameter. Please take a look at *executeGrader.sh* in the source code for an example.

### Question 4: Can I set any environment variables in my grader?
Use of environment variables as part of the grader is not prohibited but we do **prohibit** setting environment variables as part of the **Dockerfile** for security purposes. Any environment variables set in **Dockerfile** will be cleaned during runtime. Please take a look at *executeGrader.sh* to see an example of setting environment variables outside Dockerfile.

### Question 5: Will the graders be run with root access?
One of the most common issues while working with Docker graders on Coursera is due to setting up inappropriate permissions in the Dockerfile.
**Coursera's infrastructure executes Docker images as non-root users without any network access for security reasons** and its important to set permissions carefully for files/directories that will be read/written/executed inside the Docker container. Please take a look at the example **Dockerfile** to see how to set up appropriate permissions.

### Question 6: Will the graders have a hostname and ip address?
Coursera's infrastructure executes Docker images as non-root users without any network access. Graders have fixed hostname with value "somehost", and fixed ip address - "192.168.1.2", which may be helpful to mimic some network connection.


### Question 7: What are the default resources and timeouts that are configured for a grader? Can I customize them?
We expect the Docker grader image and the learner submission to be less than 8 GB in size. Please contact Coursera if you are unable to compress your grader image below that size.

When running the grader on a submission, we provide a 1GB RAM and 1 Full CPU Core i.e. ~3 compute units within Amazon EC2 (~2.5 GHz modern Intel x86 core) for all graders on our platform by default. Once we initiate grading via the provided Docker graders, we have set a default timeout of 60 minutes after which Grading is stopped and a 'Timeout' error is reported to the learners. These resources and timeouts are customizable. Please see below section on *courseraprogramming* for more information on customizing resources.

### Question 8: Are there any other example graders available?
Yes, you can find a Python-based grader template in `/DemoPythonGrader/`. This is a minimal Python grader intended to onboard instructors and can be used as a starting point for instructors to adapt to their needs. Additionally, one of our instructors in the discrete optimization course has a Python grader that might be helpful to look at: https://github.com/discreteoptimization/assignment.

### Building a Docker image.
***After setting up Docker, you can begin working on your grader source code keeping the above FAQs in mind. After you have written your grader source code based on the recommendations provided, you'll have to package it using Docker using a *Dockerfile*.***

*Please Note: Before building your Docker image for local testing, you need to update the demo grader's '[Dockerfile](https://github.com/coursera/programming-assignments-demo/blob/master/custom-graders/DemoJavaGrader/GraderFiles/Dockerfile)' according the instructions mentioned at the bottom of the Dockerfile itself.*

```sh
$ docker build -t demo_grader.v1.1 .
```
Output :
```sh
Sending build context to Docker daemon 832.4 MB
Sending build context to Docker daemon
Step 0 : FROM ubuntu:latest
.....
.....
Successfully built xxxxxxxxxx
```
### Uploading Docker Build Files
A zipped file containing a Dockerfile along with custom files can now be uploaded directly to Coursera, rather than uploading a full Docker image. A Dockerfile along with build files must be directly within the zip file, at the top level directory. Coursera will then host the Docker image building process. This feature is currently only supported via the web client

##  March 2018 alert

We are aware of issues with courseraprogramming tool. The solution right now is to manually build the tool -

```sh
$ git clone https://github.com/coursera/courseraprogramming
$ cd courseraprogramming/
$ virtualenv venv
$ source venv/bin/activate
$ python setup.py develop
$ pip install -r test_requirements.txt
```


### Common errors:

#### ERROR: virtualenv is not compatible with this system or executable

Try using pythonbrew instead of virtualenv

conda install virtualenv instead of pip install virtualenv (uninstall with pip uninstall virtualenv and then install again)

https://stackoverflow.com/questions/5904319/problem-with-virtualenv-in-mac-os-x

#### ERROR: SyntaxError: Missing parentheses in call to 'print' when running any command

Use python 2.7 instead of 3

#### \<main\> panicked at 'Could not exec grader.' in Coursera, but locally the grader works

executeGrader.sh may have Windows line endings (^M). Try changing the file to unix format.
https://stackoverflow.com/questions/64749/m-character-at-end-of-lines


#### Why am I getting a “Dockerfile: no such file or directory” error when uploading Docker Build files? The image build works locally!

Make sure that the Dockerfile and your custom files are zipped correctly. A common mistake is zipping the ***folder*** that contains the Dockerfile and your custom files, but this will not work! You ***must*** zip the files directly, rather than the folder containing the files



# Introducing 'courseraprogramming'
*courseraprogramming* is a software development toolkit that helps to develop asynchronous graders for Coursera (typically programming assignments). *courseraprogramming* is mostly meant to provide tools to simulate the production environment locally to test Docker graders effectively.

Some of the advanced features will also let you automate grader updates and customize grading timeouts and resources.

Please follow [instructions] (https://github.com/coursera/courseraprogramming) to install the toolkit before moving on to the next step.

### Testing graders locally
After building your Docker image, you'll want to test your graders locally before uploading it into production.
Docker graders are augmented in certain ways when they are run on Coursera's production environment. Instructors can simulate some of this production behavior locally while testing using our command line tool [courseraprogramming](https://github.com/coursera/courseraprogramming).

Here is a simple command to test a grader locally (Note that you have to append partId HxbKF or ov8KA):
```sh
$ export CustomGraderPath=$BASE_PATH/programming-assignments-demo/custom-graders/
$ courseraprogramming grade local demo_grader.v1.1 $CustomGraderPath/DemoJavaGrader/SampleSubmission/FactoringSampleSubmission partId HxbKF
```

**After your Docker grader passes all tests in *courseraprogramming*, it's time to upload your Docker grader. You can choose to upload the build files or the locally compiled Docker image**


### Uploading Build Files
#### 1. Zip the build file contents
 - Make sure you are in the directory containing the Dockerfile. This must be the top level directory
```sh
 $ zip -r demo_grader.zip .
```

#### 2. Upload the zipped grader file to production course
- Navigate to the authoring side of your course
- Create/Navigate to the programming assignment you want to work with
- Add/Edit the programming assignment 'Custom Grader' part you want to work with
- Click on Upload Build Files and select the .zip file created in the above step
- Wait for the grader to upload and process successfully
- Make sure you see the correct grader file associated with the programming assignment part in the dropdown list of all uploaded graders. *Note* You can also delete old unused graders by deleting the corresponding grader asset within the 'Assets' tab in the course authoring interface.
- Review and Publish the new programming assignment




### Uploading Compiled Docker Image
#### 1. Package the Docker image into a tar
```sh
$ docker save demo_grader.v1.1 > demo_grader.v1.1.tar
```

#### 2. Upload the grader to production course
- Navigate to the authoring side of your course
- Create/Navigate to the programming assignment you want to work with
- Add/Edit the programming assignment 'Custom Grader' part you want to work with
- Click on Upload Full Image and select the .tar file created in the above step
- Wait for the grader to upload and process successfully
- Make sure you see the correct grader file associated with the programming assignment part in the dropdown list of all uploaded graders. *Note* You can also delete old unused graders by deleting the corresponding grader asset within the 'Assets' tab in the course authoring interface.
- Review and Publish the new programming assignment

**Alternatively, you can upload your Docker grader directly via courseraprogramming without using the web client.**

Note: it is important to use your course ID (a base64 UUID) and not your course slug (the short name used in the URLs of the course).

```sh
$ courseraprogramming upload demo_grader.v1.1 my_Course_1D itemId123 partId456
```

To publish the newly uploaded grader, you can either: (1) **recommended** navigate to the web-based authoring tools and click "Publish", or alternatively (advanced instructors only) (2) execute:

```sh
$ courseraprogramming publish my_course_1D itemId123
```

Beware, using `courseraprogramming publish` will publish _all_ edits made to a particular item. Use with caution, and only when you know the course content (e.g. programming assignment description) will not be modified concurrently.

**Important Note**: Once a new grader is published, it takes an additional 30-35 minutes for our systems to cache the grader due to which it might take significantly more time to finish the first grading that happens on a new grader. Subsequent grading overhead is as low as 5 seconds.

In case 'Grading Fails' the first time on a new grader, it is most likely due to a timeout given the additional time it took for caching the grader. Please try resubmitting to resolve the 'Timeout' issue.

#### Testing and debugging the new programming assignment
- Click on 'View as Learner' on the top left of the authoring tools to navigate to Learner's view
- Navigate to the assignment and make some test submissions. Make sure to cover all edge cases during this testing phase.
- Links to access stdout/stderr generated by the grader should be visible for each submitted part. These links are only visible to instructors as a tool for them to test and debug their graders.
- In case you experience any problems testing in the production environment that you didn't experience while testing locally, **Please Contact partner-support@coursera.org for more support**

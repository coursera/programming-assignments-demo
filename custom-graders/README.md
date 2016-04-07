### Download the grader source code locally
```sh
$ git clone https://github.com/coursera/programming-assignments-demo.git $BASE_PATH/programming-assignments-demo
$ cd $BASE_PATH/programming-assignments-demo
```

We'll start by exploring the custom grader associated with our [demo course](https://www.coursera.org/learn/pa-on-demand).

As you might've seen in the demo course, the programming assignment has two parts expecting learners to upload java programs for :
- Factorizing a number
- Finding if a number is prime

We use a single docker grader to grade both of these parts. You can view the source code of the demo grader as shown below:
```sh
$ cd custom-graders/DemoAssignmentGrader/GraderFiles
$ ls
```

Here are the different files contained in this directory:
- FactoringGrader/*: Contains solution and test cases for Part 1 : Factorizing a number
- PrimeGrader/*: Contains solution and test cases for Part 2 : Finding if a number is prime
- executeGrader.sh: Bash script which handles the overall grading workflow.
- Grader.java: File to compare output produced by the learner's submission with the solutions.
- Dockerfile: **Instructors provide their graders encapsulated in docker images which Coursera runs in a secure and efficient manner.** Dockerfile is a text document containing sequential commands to assemble the docker grader image.

#### What is Docker?
- Efficiently encapsulates applications and the required infrastructure (Linux OS, Apache web server, mySQL)
- Used to package and distribute applications
- Packaged Docker image can be run on any host along with the packaged infrastructure
- To get started, please download docker version 1.9.1 or earlier. visit https://docs.docker.com/v1.7/


### Question 1: Where can the grader find learner's submission?
Graders will be able to find learner's submission at **/shared/submission/$fileName**.
*Instructors can customize the file name via authoring tools for ease of access.*

### Question 2: How to output grades and feedback?
Coursera's APIs will rely on the *stdout* and expect it to be a JSON object containing 'fractionalScore' and 'feedback'. Example:
```sh
{"fractionalScore": 0.2, "feedback": "You failed"}
```

- **fractionalScore**: Float value signifying the fraction of score obtained by the submission. Must be betweer 0.0 to 1.0.
- **feedback**: Text feedback provided to the learner. ***Note***: We require all graders to trim/truncate their feedback strings to be less than 64 KB.

**Important: Graders shouldn't write anything other than a single JSON object with the above specification to stdout and also make sure learners are unable to write anything to stdout.**

### Question 3: Can a single grader be used to grade multiple programming assignment parts?
Managing multiple docker images for a single course could be hard due to several reasons. Coursera recommends instructors to maintain a single grader per course. During runtime, graders can easily know which part to grade based on the unique PartId supplied as a command line parameter. Please take a look at *executeGrader.sh* in the source code for an example. 

### Question 4: Can I set any environment variables in my grader?
Use of environment variables as part of the grader is not prohibited but we do **prohibit** setting environment variables as part of the **Dockerfile** for security purposes. Any environment variables set in **Dockerfile** will be cleaned during runtime. Please take a look at *executeGrader.sh* to see an example of setting environment variables outsite Dockerfile.

### Question 5: Will the graders be run with root access?
One of the most common issues while working with docker graders on Coursera is due to setting up inappropriate permissions in the Dockerfile. 

**Coursera's infrastructure executes docker images as non-root users without any network access for security reasons** and its important to set permissions carefully for files/directories that will be read/written/executed inside the docker container. Please take a look at the example **Dockerfile** to see how to setup appropriate permissions.

### Building a docker image.
***After setting up docker, you can begin working on your grader source code keeping the above FAQs in mind. After you have written your grader source code based on the recommendations provided, you'll have to package it using Docker using a *Dockerfile*.***

*Please Note: Before building your docker image for local testing, you need to update the demo grader's '[Dockerfile](https://github.com/coursera/programming-assignments-demo/blob/master/custom-graders/DemoAssignmentGrader/GraderFiles/Dockerfile)' according the instructions mentioned at the bottom of the Dockerfile itself.*

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

### Testing graders locally
After building your docker image, you'll want to test your graders locally before uploading it into production.
Docker graders are augmented in certain ways when they are run on Coursera's production environment. Instructors can simulate some of this production behavior locally while testing using our command line tool [courseraprogramming](https://github.com/coursera/courseraprogramming).

*courseraprogramming* is a software development toolkit that helps to develop asynchronous graders for Coursera (typically programming assignments). Follow [instructions] (https://github.com/coursera/courseraprogramming) to get started.

Here is a simple command to test a grader locally:
```sh
$ export CustomGraderPath=$BASE_PATH/programming-assignments-demo/custom-graders/
$ courseraprogramming grade local demo_grader.v1.1 $CustomGraderPath/DemoAssignmentGrader/SampleSubmission/FactoringSampleSubmission
```

**After your docker grader passes all tests in *courseraprogramming*, its time to upload your docker grader via our authoring tools.**
#### 1. Package the docker image into a tar
```sh
$ docker save demo_grader.v1.1 > demo_grader.v1.1.tar
```

#### 2. Upload the grader to production course
- Navigate to the authoring side of your course
- Create/Navigate to the programming assignment you want to work with
- Add/Edit the programming assignment 'Custom Grader' part you want to work with
- Click on Upload New Grader and select the .tar file created in the above step
- Wait for the grader to upload and process successfully (*Don't refresh the page during the upload*)
- Refresh the page and make sure you see the correct grader file associated with the programming assignment part
- Review and Publish the new programming assignment

#### 3. Testing and debugging the new programming assignment
- Click on 'View as Learner' on the top left of the authoring tools to navigate to Learner's view
- Navigate to the assignment and make some test submissions. Make sure to cover all edge cases during this testing phase.
- An executorRunId should be visible within the submission history for each part that you submit. This is only visible to instructors and is not visible to learners. You can input this ID in our [debug tool](http://courseraprogramming.coursera.help/viewer/) to see what stdout/stderr logs were produced by your grader for that particular grader run. Please reach out to partner-support@coursera.org to get the password to access the tool.
- In case you experience any problems testing in the production environment that you didn't experience while testing locally, **Please Contact partner-support@coursera.org for more support**

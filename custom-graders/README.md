### Download the git repository locally
```sh
$ git clone https://github.com/coursera/programming-assignments-demo.git $BASE_PATH/programming-assignments-demo
$ cd $BASE_PATH/programming-assignments-demo
```

Lets take FactoringGrader as an example. Go through the files in the directory to get an overview.
```sh
$ cd custom-graders/FactoringGrader/GraderFiles
$ ls
```

The directory contains helper code (Grader.java, solution.txt, testCases.txt) to grade an assignment, an executable file (executeGrader.sh) which is the entry point of the grader and a Dockerfile used to generate the Docker image.

#### What is Docker?
- Efficiently encapsulates applications and the required infrastructure (Linux OS, Apache web server, mySQL)
- Used to package and distribute applications
- Packaged Docker image can be run on any host along with the packaged infrastructure
- To get started, visit https://docs.docker.com/installation/

Instructors provide their graders encapsulated in docker images which Coursera runs in a secure and efficient manner.

Before starting on docker images, lets get to know how Coursera communicates with the docker images:

###Question 1: How will the learner submission be supplied to my code?
When the docker image is run on Coursera's hosts, learner's submission is copied to /shared/submission/$fileName and made accessible to the docker code. $fileName is something that is configurable by instructors.

###Question 2: How will the docker graders convey grades and feedback to Coursera?
Coursera will read everything on stdout and expect it to be a JSON object containing 'isCorrect' and 'feedback'. Example:
{"isCorrect": false, "feedback": "You failed"}

- isCorrect: Signifies if the learner passed.
- feedback: Text feedback provided to the learner.

### Building a docker image.
```sh
$ docker build -t factoring_grader.v1.1 .
```
Output :
```sh
Sending build context to Docker daemon 832.4 MB
Sending build context to Docker daemon
Step 0 : FROM ubuntu:latest
.....
.....
Successfully built 15c3a282b939
```

### Test your docker grader locally with a sample submission.
```sh
$ export CustomGraderPath = $BASE_PATH/programming-assignments-demo/custom-graders
$ docker run --user 1000 --net none -v $CustomGraderPath/FactoringGrader/sampleSubmission/:/shared/submission -t factoring_grader.v1.1
```

Output:
```sh
{"isCorrect": true,"feedback": "Congrats! All test cases passed!"}
```

### Test graders locally using 'courseraprogramming'
Testing in Coursera's production environment is quite different from testing the graders locally. 'courseraprogramming' is a software development toolkit that helps to develop asynchronous graders for Coursera (typically programming assignments). It can be used to test the graders locally in an environment that is somewhat similar to Coursera's production environment. Follow instructions [here](https://github.com/coursera/courseraprogramming) to get started.

### Package the docker image into a tar.
```sh
$ docker save factoring_grader.v1.1 > factoring_grader.v1.1.tar
```

### Test your grader in Coursera's production environment.
###### Upload the docker grader image to the programming assignment using authoring tools
###### Navigate to the learner side of the programming assignment
###### Submit using sample solutions
###### Get the grader run IDs exposed in the learner UI
*This information is just exposed to the course instructor*
###### Use these grader run IDs as an input to this [tool](http://52.2.120.167/) to read stdout and stderr output by the docker grader
*Contact programming@coursera.org to get access credentials for the tool.*

#### Common bugs/issues:
- One of the most common issues with docker files not working on Coursera's platform is due to setting up inappropriate permissions in the Dockerfile. Coursera's infrastructure executes docker images as non-root users without any network access for security reasons and its important to set permissions carefully for files/directories that will be read/written/executed inside the docker container.
- JSON output doesn't exactly match the specified format which causes Grader failures. The docker grader should only write the JSON object specified above to stdout and nothing else. 
- Use of environment variables as part of the grader is not prohibited (i.e. you can set them in your grader files) but we do limit the ability to set environment variables as part of the 'Dockerfile' for security purposes. Hence at runtime, the grader code will not be able to access any environment variables that have been set directly in the 'Dockerfile'.

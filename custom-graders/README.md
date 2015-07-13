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

The directory contains helper code (Grader.java, solution.txt, testCases.txt) to grade an assignment, an executable file (executeGrader.sh) which is the entry poin of the grader and a Dockerfile used to generate the Docker image.

#### What is Docker?
- Efficiently encapsulates applications and the required infrastructure (Linux OS, Apache web server, mySQL)
- Used to package and distribute applications
- Packaged Docker image can be run on any host along with the packaged infrastructure
- To read about docker and setting up docker for your machine, visit ....

Instructors provide their graders encapsulated in docker images which Coursera runs in a secure and efficient manner.

Before starting on docker images, lets get to know how Coursera communicates with the docker images:

###Question 1: How will the learner submission be supplied to my code?
When the docker image is run on Coursera's hosts, learner's submission is copied to /shared/submission/$fileName and made accessible to the docker code. $fileName is something that is configurable by instructors.

###Question 2: How will the docker graders convey grades and feedback to Coursera?
Coursera will read everything on stdout and expect it to be a JSON object containing 'isCorrect' and 'feedback'. Example:
{
    "isCorrect": false,
    "feedback": "You failed"
}

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
$ docker run --user 1000 --net none -v $CustomGraderPath/FactoringGrader/sampleSubmission/:/shared/submission -t factoring_grader_v1.1
```

Output:
```sh
{"isCorrect": true,"feedback": "Congrats! All test cases passed!"}
```

### Package the docker image into a tar.
```sh
$ docker save factoring_grader.v1.1 > factoring_grader.v1.1.tar
```

### Next Steps
##### - Test your grader Coursera sandbox. Refer to the programming assignments documentation for more details.
##### - After testing graders thoroughly, graders can be linked to programming assignments in the course.

#### Common bugs/issues:
- One of the most common issues with docker files not working on Coursera's platform is due to setting up inappropriate permissions in the Dockerfile. Coursera's infrastructure executes your docker images as non-root users for security restricting network access and its important to provide appropriate permissions to files/directories that will be read/written/executed.
- JSON output doesn't exactly match the specified format.

# Download the git repository locally
$ git clone https://github.com/ngarg-coursera/programming-assignments-coursera.git $BASE_PATH/programming-assignments-coursera
$ cd $BASE_PATH/programming-assignments-coursera

# Lets see how FactoringGrader works
$ cd custom-graders/FactoringGrader/GraderFiles

# Go through the files in the directory to get an overview.

# Creating a docker image

# To read about docker and setting up docker for your machine, visit ....

Before starting on docker images, lets get to know how Coursera communicates with the docker images:

Question 1: Where will I find the learner's submission?
When your docker image is run on our hosts, we supply the learner's submission as /shared/submission/$fileName of that host and make it accessible to your code. $fileName is something you configure yourselves and irrespective of what learner's upload, their file will be renamed to your given file name.

Question 2: How will I convey grades and feedback to Coursera?
We read stdout and expect it to be a JSON object containing 'isCorrect' and 'feedback'. Example:
{
    "isCorrect": false,
    "feedback": "You failed"
}

isCorrect: Its the boolean status signifying whether the learner's submission was marked as correct or incorrect.
feedback: This is the text feedback that will be made visible to the learner.

# Build a docker image using the Dockerfile.
$ docker build -t factoring_grader.v1.1 .

Output :
Sending build context to Docker daemon 832.4 MB
Sending build context to Docker daemon
Step 0 : FROM ubuntu:latest
.....
.....
Successfully built 15c3a282b939


# Run the docker image locally.
export $CustomGraderPath = $BASE_PATH/programming-assignments-coursera/custom-graders
docker run --user 1000 --net none -v $CustomGraderPath/FactoringGrader/sampleSubmission/:/shared/submission -t factoring_grader_v1.1

Output:
{"isCorrect":true,"feedback":"Congrats! All test cases passed!"}


# Save the docker image locally.
docker save factoring_grader.v1.1 > factoring_grader.v1.1.tar

# Test this docker image on Coursera sandbox. Refer to the programming assignments documentation for more details.

Important: One of the most common issues with docker files not working on our platform is due to inappropriate permissions.
Our infrastructure executes your docker images as non-root users and its important to provide appropriate permissions to files/directories you will be reading/writing/executing.
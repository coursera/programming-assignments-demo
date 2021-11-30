FROM rocker/tidyverse:4.0.0

# Make directories for storing your files.
RUN mkdir /grader
RUN mkdir /grader/solutions

# Install common r-packages
RUN R -e "install.packages(c('RCurl', 'rjson'), repos = 'http://cran.us.r-project.org', dependencies = TRUE)"
RUN apt update && apt install -y libxt6 libxt-dev

# The commands below copy files into the Docker image.
# Main grader files
COPY main.R /grader/main.R
COPY utility_functions.R /grader/utility_functions.R
COPY grade_flipSign.R /grader/grade_flipSign.R
COPY grade_workspace.R /grader/grade_workspace.R
COPY grade_markdown.R /grader/grade_markdown.R
# Copy files for the solution
COPY solutions/* /grader/solutions/

# Important: Docker images are run without root access on our platforms. Its important to setup permissions accordingly.
# Executable permissions: Required to execute main.R
# Read/write permissions: Required to copy over the submission from shared/submission
RUN chmod a+rwx -R /grader/

# Setup the command that will be invoked when your docker image is run.
# Commands to run script
CMD ["Rscript", "grader/main.R"]
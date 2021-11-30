# ENTRYPOINT for Dockerfile

# Load package to read/write JSON files and utility functions
library("rjson")
source("grader/utility_functions.R")

Main <- function(part_id) {
  
  # Find the learner's submission ---------------------------------------------
  
  # The directory /shared/submission/ is the standard submission directory across all courses.
  # This is a readonly directory. If you'd like the students to submit a zip with multiple files,
  # please ensure that the grader first moves the files to a folder with the correct permissions to unzip.
  files <- list.files("shared/submission/")
  
  # Save the submission to /grader/ folder, which has executable permissions
  for (f in files) {
    if (tools::file_ext(f) == "R" || tools::file_ext(f) == "RData" || tools::file_ext(f) == "Rmd") {
      file.copy(file.path("shared/submission/", f), "grader/")
    } else {
      SendFeedback(0.0, "Your file may not have the right extension.")
      return()
    }
  }
  
  # You can find your unique part_id values in the Coursera Programming Assignment lesson item.
  if (part_id == "pq3nw"){
    
    source("grader/grade_flipSign.R")
    GradeFlipSign(num_test_cases = 5)

  } else if (part_id == "YOF4z") {
    
    source("grader/grade_workspace.R")
    load("grader/solutions/data_file.RData", solution_env <- new.env())
    GradeWorkspace(num_test_cases = length(ls(solution_env)))

  } else if (part_id == "Y9ll4") {
    
    knitr::purl(input = "grader/solutions/linear_reg.Rmd", output = "grader/solutions/linear_reg.R", quiet = TRUE)
    source("grader/grade_markdown.R")
    source("grader/solutions/linear_reg.R", solution_env <- new.env())
    GradeMarkdown(num_test_cases = length(ls(solution_env)))

  } else {
    SendFeedback(0.0, "Please verify that you have submitted to the proper part of the assignment.")
    stop("Cannot find matching partId. Please double check your partId's")
  }
}

# MAIN ------------------------------------------------------------------------
# Find part_id from env variables, script is re-run for each file submitted.

part_id <- Sys.getenv("partId")
#part_id <- "pq3nw" # For local testing manually enter part_id and uncomment
Main(part_id)

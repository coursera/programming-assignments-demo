# Grading of part 2:  R workspace with 3 objects x, y, and z

load("grader/solutions/data_file.RData", solution_env <- new.env())

tryCatch(load("grader/data_file.RData", submission_env <- new.env()),
         error = function(e) {
           SendFeedback(0.0, paste("Code execution failed with error: \n", e))
           stop(paste("Code execution failed with error: \n", e))
         })

GradeWorkspace <-function(num_test_cases) {
  
  if (num_test_cases >= 1) {
    test_case_penalty <- 1/num_test_cases
  } else {
    SendFeedback(0.0, "Please reach out to course staff via discussion forums, to report a grader error.")
    stop("Please update your test case value to be a whole integer greater than 0.")
  }
  
  # Determine number of tests failed ------------------------------------------
  # Loop through solution workspace objects and compare to submission workspace
  num_test_cases_failed <- 0
  final_feedback <- ""
  for (object in ls(solution_env)) {
    if (identical(submission_env[[object]], solution_env[[object]])) {
      final_feedback <- paste(final_feedback, "Passed test case for:", object, "object. Great job! \n")
    } else {
      final_feedback <- paste(final_feedback, "Failed test case for:", object, "object. Please try again! \n")
      num_test_cases_failed <- num_test_cases_failed + 1
    }
  }
  
  # Calculate score and return feedback ---------------------------------------
  total_penalty <- min(1.0, (test_case_penalty*num_test_cases_failed))
  final_fractional_score <- 1.0 - total_penalty
  
  SendFeedback(final_fractional_score, final_feedback)
}
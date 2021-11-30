# Grading of part 1: function that flips the sign of an input vector.

source("grader/solutions/flip_sign.R")

tryCatch(source("grader/flip_sign.R"),
         error = function(e) {
           SendFeedback(0.0, paste("Code execution failed with error: \n", e))
           stop(paste("Code execution failed with error: \n", e))
         })

GradeFlipSign <-function(num_test_cases) {
  
  if (num_test_cases >= 1) {
    test_case_penalty <- 1/num_test_cases
  } else {
    SendFeedback(0.0, "Please reach out to course staff via discussion forums, to report a grader error.")
    stop("Please update your test case value to be a whole integer greater than 0.")
  }

  # Generate test cases -------------------------------------------------------
  test_inputs <- lapply(1:num_test_cases, function(x) sample(1:10, size = sample(num_test_cases)))
  
  # Generate learner and solution outputs -------------------------------------
  learner_outputs <- tryCatch(lapply(test_inputs, FlipSign),
                              error = function(e) {
                                SendFeedback(0.0, paste("Code execution failed with error: \n", e))
                                stop(paste("Code execution failed with error: \n", e))
                              })
  
  solution_outputs <- lapply(test_inputs, FlipSignSolution)
  
  # Determine number of tests failed ------------------------------------------
  num_test_cases_failed <- 0
  final_feedback <- ""
  for (i in 1:num_test_cases) {
    if (identical(learner_outputs[i], solution_outputs[i])) {
      final_feedback <- paste(final_feedback, "Passed test case #", i, "Great job! \n") 
    } else {
      final_feedback <- paste(final_feedback, "Failed test case #", i, "Using an input of:", test_inputs[i], "\n")
      num_test_cases_failed <- num_test_cases_failed + 1
    }
  }
  
  # Calculate score and return feedback ---------------------------------------
  total_penalty <- min(1.0, (test_case_penalty*num_test_cases_failed))
  final_fractional_score <- 1.0 - total_penalty
  
  SendFeedback(final_fractional_score, final_feedback)
}
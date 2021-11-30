# Utility Functions

# Compile json object for sending score and feedback to Coursera
SendFeedback <- function(fractional_score, feedback) {
  df <- data.frame(fractionalScore = fractional_score, feedback = feedback)
  jsonData <- toJSON(df)
  write(jsonData, "shared/feedback.json") 
}
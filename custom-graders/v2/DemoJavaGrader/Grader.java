// Input 1: Name of file containing solutions
// Input 2: Name of the file where output from learner's program is  stored.

// `Grader` compares the two files and prints 'fractionalScore' and 'feedback' based on whether the two files match or not.

// example: If files match exactly, the output is - {"fractionalScore": 1.0, "feedback": "Congrats! All test cases passed!"}

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.FileReader;
import java.io.FileWriter;

import java.util.Map;

public class Grader {
	public static void main(String[] args) {
		// Point penalty for each failing test case. This means if more than 5 test cases fail,
		// learner will get 0.0 as his score.
		double testCasePenalty = 0.2;

		// Number of test cases failed.
		int numTestCasesFailed = 0;

		// Final fractional score
		double finalFractionalScore = 0.0;

		Map<String, String> env = System.getenv();

		// Print Evnivornment variables
		System.out.println("Environment variables: \n");
        	for (String envName : env.keySet()) {
            		System.out.format("%s=%s%n",
                              envName,
                              env.get(envName));
        	}

		boolean local = env.get("LOCAL").equals("1");

		String feedbackfile = "/shared/feedback.json";
		String richFeedbackFile = "richFeedback.html";

		if(local) {
			feedbackfile = "./shared/feedback.json";
		}

		String feedback;
		System.err.println("cwd: " + System.getProperty("user.dir"));
		try {
			BufferedReader assignmentSolution = new BufferedReader(new FileReader(args[0]));
			BufferedReader learnerSolution = new BufferedReader(new FileReader(args[1]));

			String input;
			String output;

			for (input = assignmentSolution.readLine(), output = learnerSolution.readLine();
				input != null && output != null;
				input = assignmentSolution.readLine(), output = learnerSolution.readLine()) {
				if (!input.equals(output)) {
					numTestCasesFailed++;
				}
			}

			if (input != null || output != null) {
				finalFractionalScore = 0.0;
				feedback = "Invalid output. The number of lines produced by your code are not valid.";
			} else if (numTestCasesFailed > 0) {
				// We're penalizing testCasePenalty for each test case failed.
				double totalPenalty = Math.min(1.0, (testCasePenalty * numTestCasesFailed));

				finalFractionalScore = 1.0 - totalPenalty;
				feedback = "Your solution failed " + numTestCasesFailed + " test cases. Please try again!";
			} else {
				finalFractionalScore = 1.0;
				feedback = "Congrats! All test cases passed!";
			}

			assignmentSolution.close();
			learnerSolution.close();

		} catch(IOException io) {
			System.err.println("Got an exception!");
			System.err.println(io.getMessage());
			io.printStackTrace(System.err);
			feedback = io.getMessage();
		}

	
		// Construct jsonOutput in the format expected by Coursera's infrastructure.

		// fractionalScore must be between 0.0 to 1.0.
		String feedbackStdout = feedback + " (GrID V2 stdout)";
		String jsonOutput = "{" + "\"fractionalScore\":" + finalFractionalScore + "," + "\"feedback\":" + "\"" + feedbackStdout + "\"" + "}";
		System.out.println(jsonOutput);

		try {
			BufferedWriter writer = new BufferedWriter(new FileWriter(feedbackfile));
			String feedbackUpdated = feedback + " (GrID V2 feedback)";
			jsonOutput = "{" + 
				"\"fractionalScore\":" + finalFractionalScore + "," + 
				"\"feedback\":" + "\"" + feedbackUpdated + "\"" + "," +
				"\"richFeedbackFile\":" + "\"" + richFeedbackFile + "\"" +
			    "}";
			writer.write(jsonOutput);
			writer.close();	

			String richFeedbackpath = "";
			if(local) { 
				richFeedbackpath = "./shared/" + richFeedbackFile;
			} else {
				richFeedbackpath = "/shared/" + richFeedbackFile;
			}
			BufferedWriter richWriter = new BufferedWriter(new FileWriter(richFeedbackpath));
			String richFeedback = "<html><head><title> Rich Feedback</title></head><body><h1>Rich Feedback</h1><ul><li><font color=green>Green feedback</font></li><li><font color=red>Red feedback</font></li></ul></body></html>";
			richWriter.write(richFeedback);
			richWriter.close();
                } catch(IOException io) {
                        System.err.println("Got an exception writing to feedback.json!");
                        System.err.println(io.getMessage());
                        io.printStackTrace(System.err);
                        feedback = io.getMessage();
                }
	}
}

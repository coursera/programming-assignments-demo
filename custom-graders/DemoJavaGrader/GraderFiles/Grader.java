// Input 1: Name of file containing solutions
// Input 2: Name of the file where output from learner's program is  stored.

// `Grader` compares the two files and prints 'fractionalScore' and 'feedback' based on whether the two files match or not.

// example: If files match exactly, the output is - {"fractionalScore": 1.0, "feedback": "Congrats! All test cases passed!"}

import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileReader;

public class Grader {
	public static void main(String[] args) {
		// Point penalty for each failing test case. This means if more than 5 test cases fail,
		// learner will get 0.0 as his score.
		double testCasePenalty = 0.2;

		// Number of test cases failed.
		int numTestCasesFailed = 0;

		// Final fractional score
		double finalFractionalScore = 0.0;

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
		String jsonOutput = "{" + "\"fractionalScore\":" + finalFractionalScore + "," + "\"feedback\":" + "\"" + feedback + "\"" + "}";
		System.out.println(jsonOutput);
	}
}

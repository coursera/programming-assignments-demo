// Input 1: Name of file containing solutions
// Input 2: Name of the file where output from learner's program is  stored.

// `Grader` compares the two files and prints 'isCorrect' and 'feedback' based on whether the two files match or not.

// example: If files match exactly, the output is - {"isCorrect": true, "feedback": "Congrats! All test cases passed!"}

import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileReader;

public class Grader {
	public static void main(String[] args) {
		int numTestCasesFailed = 0;
		String feedback;
		boolean isCorrect = false;
		try{
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
				feedback = "Invalid output. The number of lines produced by your code are not valid.";
			} else if (numTestCasesFailed > 0) {
				feedback = "Your solution failed " + numTestCasesFailed + " test cases. Please try again!";
			} else {
				isCorrect = true;
				feedback = "Congrats! All test cases passed!";
			}
			
			assignmentSolution.close();
			learnerSolution.close();

		} catch(IOException io) {
			feedback = io.getMessage();
		}

		// Construct jsonOutput in the format expected by Coursera's infrastructure.
		String jsonOutput = "{" + "\"isCorrect\":" + isCorrect + "," + "\"feedback\":" + "\"" + feedback + "\"" + "}";
		System.out.println(jsonOutput);
	}
}

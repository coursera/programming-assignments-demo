// Input 1: Name of file containing solutions
// Input 2: Name of the file where output from learner's program is  stored.

// `Grader` compares the two files and prints 'fractionalScore' and 'feedback' based on whether the two files match or not.

// example: If files match exactly, the output is - {"fractionalScore": 1.0, "feedback": "Congrats! All test cases passed!"}

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.FileReader;
import java.io.FileWriter;
import java.net.*;
import java.io.*;
import java.util.*;
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

		// Printing to Standard Error (which will show up in logs)
		// for debugging.
		System.err.println("This is an example standard error");

		// Print Evnivornment variables
		System.out.println("Environment variables:");
        	for (String envName : env.keySet()) {
            		System.out.format("%s=%s%n",
                              envName,
                              env.get(envName));
        	}

		String feedback;
		System.out.println("cwd: " + System.getProperty("user.dir"));
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

		try {
			// feedback.json file is required and needs to be updated as a last step of the grading.
			// This file needs to be in /shared/ folder. Coursera's autograder infrastructure 
			// uses this as evaluation, and shown to the learners appropriately.
			String feedbackfile = "/shared/feedback.json";
			BufferedWriter writer = new BufferedWriter(new FileWriter(feedbackfile));
			String feedbackUpdated = feedback + " (GrID V2 feedback)";
			// Construct jsonFeedback in the format expected by Coursera's infrastructure.
			// fractionalScore must be between 0.0 to 1.0.

			// Providing rich feedback in a separate file is possible and is completely optional.
			// Currently supported rich feedback types are : HTML and TXT.
			// If the grader is producing rich feedback, it's type need to be specified feedback.json
			// richFeedbackType field is optional, if it provided, then the grader is expected
			// to provide corresponding rich feedback file in the /shared/ folder.
			// The following example demonstrates using HTMl rich feedback.
			String jsonFeedback = "{" +
				"\"fractionalScore\":" + finalFractionalScore + "," +   // Required field.
				"\"feedback\":" + "\"" + feedbackUpdated + "\"" + "," + // Required field.
				"\"feedbackType\":" + "\"HTML\"" +                  	// Optional field.
			    "}";
			System.out.println("Feedback: ");
			System.out.println(jsonFeedback);
			writer.write(jsonFeedback);
			writer.close();	

			// Like feedback.json, htmlFeedback.html should exist /shared/ folder if the json feedback
			// above has the field richFeedbackType is set to "HTML" (similarly txtFeedback.txt for "TXT" type).
			// Most importantly if there is richFeedback learner will not see "feedback" provided in the json, however
			// this field is required for backward compatibility, but the value can be empty. 
			String richFeedbackFilePath = "/shared/htmlFeedback.html";

			// In this example we are also showing an example to make network calls and merely copying to rich feedback file.
			download("https://github.com/", richFeedbackFilePath);
                } catch(IOException io) {
                        System.err.println("Got an exception writing feedback to file!");
                        System.err.println(io.getMessage());
                        io.printStackTrace(System.err);
                        feedback = io.getMessage();
                }
	}

	private static void download(String url, String filePath) {
		try {

		    URL urlObj = new URL(url);
		    URLConnection urlCon = urlObj.openConnection();

		    InputStream inputStream = urlCon.getInputStream();
		    BufferedInputStream reader = new BufferedInputStream(inputStream);

		    BufferedOutputStream writer = new BufferedOutputStream(new FileOutputStream(filePath));

		    byte[] buffer = new byte[4096];
		    int bytesRead = -1;

		    while ((bytesRead = reader.read(buffer)) != -1) {
			writer.write(buffer, 0, bytesRead);
		    }

		    writer.close();
		    reader.close();

		    System.out.println("Web page saved");

		} catch (MalformedURLException e) {
		    System.out.println("The specified URL is malformed: " + e.getMessage());
		} catch (IOException e) {
		    System.out.println("An I/O error occurs: " + e.getMessage());
		}	
	}
}

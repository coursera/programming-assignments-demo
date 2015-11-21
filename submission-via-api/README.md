Instructors may want to use our submission API directly within their assignment rather than having learners upload their solution files via our web UI.

This use case might particularly be useful for instructors who want to integrate the submission workflow with the development environment itself for faster edit-submit cycles. This requires instructors to hook up Coursera's submission API inside the development environment they deliver to the learners.

The API

POST
www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1

Body:  
```
{  
	/**  
	 * unique ID to identify a particular programming assignment on our platform.  
	 * This should be included while calling our submit APIs for us to identify the assignment  
	 * to which the learner intends to submit.  
	 *  
	 * assignmentKey is a unique Id associated with each API based programming assignment.   
	 * This can be obtained by the course team via the programming assignment authoring UI under  
	 * the `AssignmentId` field.
	 */  
	"assignmentKey": String,  
  
	/**  
	 * Learner's coursera email Id.  
	 */  
	"submitterEmail": String,  
  
	/**  
	 * Secret token issued to a learner with an expiry time.   
	 * Learner must input its secret token while submitting via our APIs for authorization  
	 * along with their emailId.   
	 * This token can be obtained by each learner from the assignment page under 'How to submit' section.  
	 */  
	"secret": String,  
  
	/**  
	 * Contains the list of all parts in the assignment and 'Not' just the submitted ones.  
	 */  
	"parts": {  
		/**  
		 * PartId is the unique ID associated with each individual part inside the programming assignment.  
		 * This is exposed to the course team via the programming asisgnment authoring UI  
		 * under the `PartId` field for each part.  
		 */   
		"$PartId1": {  
			/**  
			 * `output` contains the learner's submission as a single String.  
			 * If the learner chose not to submit a particular part, `output` should not be present  
			 * for that part.  
			 */  
			"output": String  
		},  
  
		/**  
		 * Example of including a part that wasn't submitted by a learner.  
		 */  
		 "$PartId2": {  
		 	/**  
		 	 * Empty Json not including `output`.  
		 	 */  
		 }  
		... similarly for other parts if any  
	}  
}  
```

cUrl command:  
```
curl -X POST -H "Cache-Control: no-cache" -H "Content-Type: application/json" -d '{  
  "assignmentKey": $assignmentKey,  
  "submitterEmail": $learnerEmail,  
  "secret": $learnerSecret,  
  "parts": {  
    "$partId1": {  
      "output": "$learnerSubmission"  
    }  
  }  
}' 'https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1'  
```


Returns:  
  
HTTP Code: 200 (Ok)  
```  
{  
	"elements": [{  
	  	"id": String,  
		"courseId": String,  
	    "itemId": String,  
	    "evaluation": {  
	    	/**  
	    	 * Contains the overall score associated with the whole submission.  
	    	 * Only present if evaluation for all submitted parts has been completed.  
	    	 */  
		  	"score":Int,  
  
		  	/**  
		  	 * Maximum score for this assignment.  
		  	 */  
			"maxScore": Int,  
  
			/**  
			 * Minimum overall score required to pass this assignment.  
			 */  
			"passingScore": Int,  
  
			/**  
			 * Individual part evaluations.  
			 */  
		 	"parts": {  
				"$partId1": {  
					/**  
					 * Title of the part as specified by the instructors  
					 */  
					"title": String,  
  
					/**  
					 * Order at which this part appears in the assignment.  
					 */  
					"order": Int,  
  
					/**  
					 * Maximum score attainable for this part.  
					 */  
					"maxScore": Int,  
  
					/**  
					 * Boolean value indicating if this particular part was submitted.  
					 */  
					"isSubmitted": Boolean,  
  
					/**  
					 * If submitted, each part can be evaluated on runtime or after a delay  
					 * depending on the type of grader for each part.  
					 *  
					 * isScored indicates if the evaluation of this particular part is finished.  
					 */  
					"isScored": Boolean,  
  
					/**  
					 * `score` obtained by the learner.  
					 * Only present if `isScored` is true.  
					 */  
					"score": Int,  
  
					/**  
					 * `feedback` obtained by the learner.  
					 * Only present if `isScored` is true.  
					 */   
					"feedback": String,  
				},  
				... similarly for all other parts in the assignment.  
			}  
		}  
	}],  
	"paging": null,  
  	"linked": null  
}  
```
  
HTTP Code: 401 (Unauthorized) if the emailId or the ‘secret’ is invalid.  
```
{  
  "message": "Invalid email or token.",  
  "details": {  
    "learnerMessage": "Invalid email or token."  
  }  
}  
```

HTTP Code: 400 (Bad Request) if a ‘secret’ from a different assignment is used.  
```
{  
  "message": "Token is for a different assignment",  
  "details": {  
    "learnerMessage": "You used a token for $itemName in $courseName. Please use a token for the assignment you are submitting."  
  }  
}  
```

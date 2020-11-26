
Coursera programming assignment submissions can be made within the lab environment through pre-built submit button or any custom way using lab submssion API.

Lab Submission API 

POST https://hub.coursera-apps.org/api/workspaceSubmissions.v1?action=createBatch

Body:

```
{  
	/**  
	 * Submission token issued to a learner with an expiry time when lab is launched. 
	 * The token can be obtained in cookies 'COURSERA_SUBMISSION_TOKEN' 
	 */  
	"token": String,
  	
  	/**
  	 * Submision schemas are defined in assginemnt authoring page. Specify the schema
  	 * you want to use here. Note that these schema names can be only from one assignment.
  	 */
  	"schemaNames": [String, String, ...]
}
```

cUrl command:

```
curl -X POST -H "Cache-Control: no-cache" -H "Content-Type: application/json" -d '{  
  "token": $token,  
  "schemaNames": [$schemaName1, $schemaName2]    
}' 'https://hub.coursera-apps.org/api/workspaceSubmissions.v1?action=createBatch'
```

Returns:

HTTP Code: 200 (Ok)

```
{  
	/**
	 * Submission result message
	 */
	"message": String
}
```

HTTP Code: 403 (Forbidden) if submission token is invalid.

```
{  
	"message": "Invalid submission token",  
}
```

HTTP Code: 400 (Bad Request) if a submission schema name doesn't exist.

```
{  
	"message": "Could not find schema with name $schemaName",  
}
``` 
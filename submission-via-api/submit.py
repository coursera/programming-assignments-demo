import requests, json

def submit(submitterEmail,secret,key,submission_part,all_parts, data):
        submission = {
                    "assignmentKey": key,
                    "submitterEmail":  submitterEmail,
                    "secret":  secret,
                    "parts": {}
                  }
        for part in all_parts:
            if part == submission_part:
                submission["parts"][part] = {"output": data}
            else:
                submission["parts"][part] = dict()

        response = requests.post('https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1', data=json.dumps(submission))

        if response.status_code == 201:
            print ("Submission successful, please check on the coursera grader page for the status")
        else:
            print ("Something went wrong, please have a look at the reponse of the grader")
            print ("-------------------------")
            print (response.text)
            print ("-------------------------")



key = "Tdma9jdAEead7w5LqXvQQQ" # Assessment key found on the authoring side (top of page)
all_parts = ["HxbKA","ov8KV"] # Part IDs found on the authoring side 

email = "your-email@instructor.com" #your instructor email 
secret = "learner-token" #learner token found on the learner side of the assessment (token changes every 30 minutes)

# or ask learner for their email/secret when they run submit.py
# email = raw_input("What is your Coursera email?\n")
# secret = raw_input("What is your Coursera token? (please find this on the assessment page)\n")

part = "HxbKA" #part ID for part 1 of this example assessment

with open('test.base64', 'r') as myfile: #test.base64 is the learner submission
    data = myfile.read()

submit(email, secret, key, part, all_parts, data)

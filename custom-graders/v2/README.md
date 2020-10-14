# New V2 Format Custom grader samples

### What is new in V2?
Please refer to this [doc](https://docs.google.com/UPDATE_THE_LINK) to know more about what is available in autograder v2.

### Demo Java Grader

DemoJavaGrader is one custom grader sample demonstrates what mainly changed in autograder v2.

Graders now need to produce ``feedback.json`` in ``/shared`` folder in the same format as before, which is : 
```sh
{"fractionalScore": 0.2, "feedback": "You failed"}
```

### Demo Java Grader With Rich Feedback

In V2, we now support rich feedback. DemoJavaGraderWithRichFeedback demonstrates how to provide rich feedback. This is an optional feature. If graders decides to provide rich feedback, then we only show rich feedback to the learner.

Custom grader can indicate rich feedback, by providing the optional field "feedbackType" in ``feedback.json``. This can take either "HTML" or "TXT" as values. It is also important for the grader to provide the rich feedback in ``/shared/`` folder, ``htmlFeedback.html`` for "HTML" and ``txtFeedback.txt`` for "TXT" respectively.

```sh
{"fractionalScore": 0.2, "feedback": "You failed", "feedbackType": "HTML"}
```

### Demo Java Grader With Network

In V2, coursera can access certain predefined domains, from the the grader. This example demonstrates downloading coursera.org page into ``/shared/htmlFeedback.html`` and provide this as rich feedback. 

### Demo Python Grader

In V2, parameters to the custom graders are now passed as environment variables, as opposed to command line arguments (in v1). This example demonstrates getting partId as an environment vairable.


# Introducing 'coursera_autograder'

[*coursera_autograder*] (https://github.com/coursera/coursera_autograder/blob/master/README.rst) is a replacement for *courseraprogramming* to test and upload v2 graders.


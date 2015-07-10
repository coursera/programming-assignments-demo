## Built-in graders

Built-in graders are Coursera provided programming assignment graders. They are called built-in since they are built into our systems and instructors only need define a simple configuration to create these graders. Apart from that, these graders are fairly simple in nature due to which, they compute learner's submissions and provide feedback/grades at runtime unlike 'Custom graders' which return feedback/graders after a small delay.

We currently support two types of built-in graders.

#### (1) Numeric Interval Graders

Its a simple grader that expects a list of numbers from the learner, and grades/provides feedback by matching each number to a given set of intervals.

#### (2) Regular Expression Graders

This grader expects a string from the learner as a submission, and grades/provides feedback based on which regular expression did the learner's submission match.


#####Examples of each type of grader can be found in the sub-folders of this directory.

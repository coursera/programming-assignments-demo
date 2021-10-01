# Configurable Grader Template for Python assignments

This is a minimal template for using the <b>configurable built-in grader</b> type on Lab Programming Assignments using VSCode.

Built-in lab graders enable educators to create custom grading logic without any offplatform build. All of the autograder creation and testing can be done in the Coursera platform.

This template was created to introduce partners to the minimum requirements for implementing a configurable grader. It is meant to serve a starting point and a functional example, using the Python programming language. It is not designed to dictate the sole strategy for designing a configurable grader.

Prior to reviewing this template, we strongly recommend reviewing the [Educator Resource Center article](https://www.coursera.support/s/article/4402955530011-Use-Built-In-Graders-to-Create-Autograded-VSCode-Lab-Assignments?language=en_US) about creating a configurable grader.

# Table of Contents
1. [Using this template as a working exmaple in your test course](#using-this-template-in-your-test-course)
2. [Template grader contents](#template-grader-contents)
3. [Template grader workflow](#template-grader-workflow)

For additional questions about setting up a configurable grader, please reach out to your partner support team.


# Using this template in your test course

To set up this template as a functional assignment in your test course, please follow these steps:

1. Set up a VSCode base image with configurable grader. To do this, go to Lab Manager and follow Step 1 instructions [here](https://www.coursera.support/s/article/4402955530011-Use-Built-In-Graders-to-Create-Autograded-VSCode-Lab-Assignments?language=en_US). 
2. In the newly created and published image, add a Lab. 
3. Open your new Lab, and populate the folders `/autograde` and `/learn` with the contents of this template.
4. Return to Lab Manager, and click Publish.
5. Connect your lab to a programming assignment following Step 5 instructions [here](https://www.coursera.support/s/article/4402955530011-Use-Built-In-Graders-to-Create-Autograded-VSCode-Lab-Assignments?language=en_US). 

    Note that you should have two parts configured with the following parameters:

    <b>Lab Configuration</b>
Content path (optional): `/?folder=/home/coder/project/learn`

    <b>Part parameters for `flipSign`</b>
    * Part title: flipSign
    * Learner submission file/folder path: `/home/coder/project/learn/flipSign/flipSign.py`
    * Grader file path: `home/coder/project/autograde/multiply/grader.py`

    <b>Part parameters for `multiply`</b>
    * Part title: multiply
    * Learner submission file/folder path: `/home/coder/project/learn/flipSign/flipSign.py`
    * Grader file path: `home/coder/project/autograde/multiply/grader.py`

6. Publish the programming assignment.
7. Click 'View as learner' and submit assignment. We encourage you to try a variety of submissions to see the kinds of feedback we've coded into this template.

The next sections describe how this template was designed, and explain how you may adjust the code to fit your unique course needs.

# Template grader contents

This configurable grader template autogrades learner submissions with the following steps:

## /autograde

In each `/home/coder/project/autograde/<partGrader>`, there is a `grader.py` and `solution.py`. `grader.py` is the core grading script for that part (note this template has two parts/problems for learners to solve -- `flipSign` and `multiply`). Each one is also a separate Part in the Programming Assignment lesson item in the Coursera course shell. <i>Part IDs are not needed in this implementation.</i> The `solution.py` contains the solution for each part, and is referenced by `grader.py`, to compare how the learner submission compares to the instructor solution.

The `/autograde` folder and its contents are not visible to learners. It is only visible in the instructor lab.

## /learn
In each `/home/coder/project/learn/<part>`, there is starter code for learners to use. In this partner-facing template, we include some commentary so that you can test this functional template with some intentionally incorrect/buggy code. When you then submit the incorrect code as a learner, you should see examples of actionable feedback. We strongly recommend that you include clear, actionable feedback for your learners so that they understand the steps they need to take to improve their work.

The `/learn` folder and its contents are visible to all learners. It is the appropriate place for any and all learner-facing material.


# Template grader workflow
 Below lists the high-level steps captured in each `grader.py`, where much of the core grading logic is.

0. Some initial container set up is completed, such as setting parameters depending on whether the grading code is executed in the instructor lab environment (through Lab Manager) or in autograding (i.e. when submitting as a learner). This template has been written to function in both environments, to ease testing.
1. The learner submissions are ingested from `/home/coder/project/learn/<problem>` folders. Note that when testing the autograder from the instructor lab, this template is set up to pull the starter code available in `learn/<problem>`.
2. Test learner submission for any exceptions that prevent it from running. If there are exceptions, this is caught and sent as feedback, with a zero score, to `/shared/feedback.json`. Note that you can write to `/shared/feedback.json` in both instructor lab and autograding. It is a <b>requirement</b> to send final learner feedback to this file in autograding.
3. If there are no exceptions, randomly generate test cases. Run both the learner submission and instructor solution against these test cases. Compare results case by case, and tally up the score.
4. If the learner solution misses any test cases, compile string feedback indicating which test case, and what the expected output was. 
5. Compile feedback and send to `/shared/feedback.json`.

Note that in your own implementation, you will likely need to adjust code relevant to steps 3 and 4, especially if your test cases are not of the same format, are more complex, or are not randomly generated.

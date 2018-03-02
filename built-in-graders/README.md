## Built-in graders

Built-in graders are Coursera provided programming assignment graders and are simpler to set up than custom graders. In this model, learners run code in their local environment and submit the output on Coursera. Their output is checked against a set of numeric values, numeric ranges, or regular expressions provided by you. Learners receive grades and feedback immediately.

Built-in graders support two types of logic: numeric and regular expression.

#### (1) Numeric Graders

In this numberic graders, a learner inputs a single line list of real numbers separated by whitespace. The learner output needs to match the grader conditions. Graders can have several conditions that attach a correct/incorrect status with feedback. 

#### (2) Regular Expression Graders

In the regular expression graders, learners need to submit a text string. The grader accepts any answer that matches a defined pattern. For example, a regular expression grader might accept any answer that:

- Contains one or more specific strings (words, phrases, or sequences of letters)
- Doesn't contain one or more specific strings (words, phrases, or sequences of letters)
- Meets or exceeds a specific character count

#### Examples of each type of grader can be found in the sub-folders of this directory.

Built-in graders can be directly built using our authoring interface. To learn more about built-in graders, please review [this article on built in graders](https://partner.coursera.help/hc/articles/205314475) in the Partner Resource Center.

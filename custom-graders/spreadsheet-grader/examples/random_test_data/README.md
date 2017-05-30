# Grader with random-number test data

This example demonstrates using random numbers to 'fuzz test' learner submissions. While all values in the template spreadsheet are static, the grader spreadsheet replaces values in the `_data` sheet with random values. If a learner has written the correct formula, their calculation will agree with grader spreadsheet calculations. 

```
score: 0.6 / 1.0

+--------------+---------------+----------+
| Value        | Correct Value | Feedback |
+--------------+---------------+----------+
| 1.6385721442 | 1.6385721442  | Correct  |
| 2.5          | 2.2805965099  | Too High |
| 3.5          | 3.4321545159  | Too High |
| 4.8850383347 | 4.8850383347  | Correct  |
| 5.781772467  | 5.781772467   | Correct  |
+--------------+---------------+----------+
```

Since random values change on each grading attempt, a learner who copies the correct value from a prior submission will not be marked correct.
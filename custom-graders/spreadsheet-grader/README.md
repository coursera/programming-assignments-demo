# Configurable spreadsheet autograder

This dockerized autograder evaluates a learner-submitted spreadsheet with grader spreadsheet authored by an instructor. The basic procedure is as follows:

    1) Open the learner and instructor spreadsheets. 
    2) Copy grader formulas from the grader spreadsheet to the learner spreadsheet, adding sheets if absent.
    3) Read the top-left cell from the `_score` sheet. This is the overall submission score.
    4) Read values `_feedback` and format as an ASCII table. This is the feedback text that the learner will see.

See example submission / grader spreadsheet pairs in the `examples` directory. To build and run locally using Docker, do:
```
./build.sh
docker run -v `pwd`/examples/simple_matching:/shared
```

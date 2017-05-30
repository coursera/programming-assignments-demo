# Pseudo - macros

Unfortunately, our grading system is not compatible with user-defined Macros. To work around this, we are experimenting with a pseudo-macro scheme wherein the replaces some user formulas with evaluated Python functions targeted on the input cell. 

For example, suppose you want to check if cell text is underlined. There is no built-in function for checking underline status, but this data _is_ stored within the cell. Within a normal spreadsheet, a user-defined macro could be used to add this behavior:

```
Function CharUnderline(aRange As Variant) As Integer
    CharUnderline = ThisComponent.Sheets(0).getCellRangeByName(aRange).CharUnderline
End CharUnderline
```
Then, to get the underline status of cell `A1` do:
```
=CharUnderline(A1)
```

Since user-defined macros don't work within the autograder environment, our hack is to define a set of named 'pseudo-macros' that expose cell properties like `CharUnderline`, which can be used to extract cell properties. You can examine the implementation within `custom-graders/spreadsheet-grader/psuedo_macros.py` to see a complete list of supported property accessors. 

To use one these pseudo-macros, write a formula like:
```
=CharUnderline($submission.A1)
='CharUnderline'($submission.A1)
='CharUnderline'*($submission.A1)
```
All of these will do the same thing in the autograding environment, namely get the `CharUnderline` property of cell `A1` within the `submission` sheet. 

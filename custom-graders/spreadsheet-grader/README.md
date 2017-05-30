# Configurable spreadsheet autograder #

This 


Procedure:
    1) Check instructor spreadsheet (must include sheets named _score and _feedback)
    2) Check learner spreadsheet (must include sheets with names matching all non-underscored sheets in instructor spreadsheet)
    3) Append instructor sheets with underscore to learner spreadsheet, evaluate.
    4) Get _feedback sheet value, format as table.
    5) Get _score sheet value, verify is single value.
    6) Return result

Error messages:
    If _score sheet missing, "Instructor file must have a sheet titled '_score'."
    If _feedback sheet missing, "Instructor file must have a sheet titled '_feedback'."
    If [submission] sheet missing, "Submission must include a sheet titled 'submission'"



docker run -it -v `pwd`/grader/:/shared/input/grader/ -v `pwd`/submission/:/shared/input/submission/ coursera/grader/spreadsheet

soffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault  --headless &

http://pydoc.net/Python/unotools/0.3.0/unotools.component.calc/
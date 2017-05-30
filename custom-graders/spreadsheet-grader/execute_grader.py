import subprocess
import time
import json
import sys
import os

from shutil import copyfile

from unotools import Socket, connect
from unotools.component.calc import Calc
from unotools.unohelper import convert_path_to_url

from pseudo_macros import evaluate_macro

from prettytable import PrettyTable

def emit_evaluation(fractionalScore, feedback_string):
    # stdout is reserved for the final evaluation. System expects JSON-format 
    # with fields 'fractionalScore' and 'feedback'
    print(json.dumps({
        'fractionalScore': fractionalScore, 
        'feedback': feedback_string
    }))


def log(message):
    # Since stdout is reserved for final evaluation data, log messages must be printed to stderr
    sys.stderr.write(message)


def trim_cell_forumulas(forumulas):
    def reversed_generator():
        all_previous_empty = True
        for row in reversed(forumulas):
            last_col = len(row) - next((i for i, v in enumerate(reversed(row)) if len(v) > 0), len(row))
            if last_col > 0:
                all_previous_empty = False
            if not all_previous_empty:
                yield row[:last_col]
    return list(reversed(list(reversed_generator())))


def get_sheet_formulas(sheet):
    # For simplicity, we read formulas from a large range of cells to make sure
    # that we've got everything. Because this range is hard-coded and broad, we
    # expect most of these cells to be empty. Open office cell value updates 
    # are relatively slow, however, so we don't want to insert empty values. To
    # avoid this, we proactively trim our formulas.
    return trim_cell_forumulas(
        sheet.get_cell_range_by_name('A1:Z500').get_formula_array())


def get_feedback_data(graded_submission):
    # Read data from the '_feedback' sheet and return values a rectangular array
    feedback_sheet = graded_submission.get_sheet_by_name('_feedback')
    formulas = get_sheet_formulas(feedback_sheet)
    column_count = len(formulas[0])
    return [
        [feedback_sheet.get_cell_by_position(i, row).String for i in range(column_count)]
        for row in range(len(formulas))
    ]


def get_feedback_string(graded_submission):
    # Read data from '_feedback' and format as human-readable ASCII table. 
    feedback_data = get_feedback_data(graded_submission)
    table = PrettyTable()
    table.field_names = feedback_data[0]
    for row in feedback_data[1:]:
        table.add_row(row)
    table.align = 'l'
    return str(table)

def get_open_office_context():
    oofice = subprocess.Popen([
        'soffice',
        '--accept=socket,host=localhost,port=2002;urp;',
        '--norestore',
        '--nologo',
        '--nodefault',
        '--headless'])
    time.sleep(2)  # Sleep allow oofice to boot up
    return connect(Socket('localhost', '2002'))

def load_spreadsheet(context, path, filename):
    mountedPath = os.path.join('shared', path)
    if not os.path.exists(mountedPath):
        raise Exception('Expected to find a file at {}'.format(mountedPath))
    # Copy files to avoid locking conflict in the mounted filesystem
    copyfile(mountedPath, filename)
    return Calc(
        context,
        convert_path_to_url(filename))

def main():
    # Start open office
    context = get_open_office_context()
    # Load the submission and grader
    submission = load_spreadsheet(context, 'submission/submission.xlsx', 'submission.xlsx')
    try:
        grader = load_spreadsheet(context, 'grader/grader.ods', 'grader.ods')
    except:
        grader = load_spreadsheet(context, 'grader/grader.xlsx', 'grader.xlsx')

    # Get names of grader sheets (starting with '_') that will be added to the submission spreadsheet
    grader_replacement_names = [name for name in grader.sheets.get_element_names() if name.startswith('_')]

    for name in grader_replacement_names:
        # Extract formula values from the grader sheet
        grader_formulas = trim_cell_forumulas(
            grader.get_sheet_by_name(name)
                  .get_cell_range_by_name('A1:Z500')
                  .get_formula_array())
        # Add a new blank sheet to the submission, if the sheet does not exist
        if not submission.sheets.hasByName(name):
            submission.insert_sheets_new_by_name(name, submission.get_sheets_count())
        submission_sheet = submission.get_sheet_by_name(name)
        # Insert formulas from the grader sheet into the submission sheet
        for r, row in enumerate(grader_formulas):
            for c, formula in enumerate(row):
                # Check to see if there is a macro value associated with the formula
                macro_value = evaluate_macro(submission, submission_sheet, formula)
                if macro_value is not None:
                    formula = str(macro_value)
                submission_sheet.get_cell_by_position(c, r).setFormula(formula)

    # Score is the value of the top-left cell of the '_score' sheet in the decorated submission file
    score = submission.get_sheet_by_name('_score').get_cell_by_position(0, 0).Value

    # Feedback is a text version of the '_feedback' sheet in the decorated submission file
    feedback_string = get_feedback_string(submission)

    log('\n\n********************* Start Summary ******************************\n')
    log('score: {} / 1.0\n\n'.format(score))
    log(feedback_string)
    log('\n******************** End Summary **********************************\n\n')

    emit_evaluation(score, feedback_string)

if __name__ == '__main__':
    main()
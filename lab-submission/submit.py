import json
import re
import requests


COURSERA_SUBMISSION_URL = 'https://hub.coursera-apps.org/api/workspaceSubmissions.v1?action=createBatch'


def submit(submission_token, schema_names):
    """
    Make a request to lab submission api and handle response.

    Parameters
    ----------
    submission_token: string
        value of COURSERA_SUBMISSION_TOKEN from cookies
    schema_names: array of strings
        submission schema names defined in programming assignment authoring
    """
    try:
        response = requests.post(
            COURSERA_SUBMISSION_URL,
            data=json.dumps({'token': submission_token, 'schemaNames': schema_names}),
            timeout=10,
        )
    except Exception as err:
        return 'Failed to execute submission request: {}'.format(err)

    if response.status_code == 201:
        return response.json()['elements'][0]['message']
    elif response.status_code == 200:
        return response.json()['message']
    elif response.status_code < 500:
        return 'Bad request:\n{}'.format(response.json())
    else:
        error_id, = re.findall(
            'This exception has been logged with id <strong>(.+)</strong>',
            response.text)
        return 'Unexpected server error logged with id {}. '.format(error_id) + \
               'Please contact Coursera support.'


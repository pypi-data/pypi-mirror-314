"""
The custom logic for the command m3 report.

This logic is created to convert parameters from the Human readable format to
appropriate for M3 SDK API request.
"""


def create_custom_request(request):
    if request.parameters.get('reportProjectType') != 'ACCOUNT' and \
            request.parameters.get('eoAccount'):
        raise AssertionError(
            "The \'account-id\' parameter may be specified only in case "
            "ACCOUNT report-type is set. Account-id is not applicable with "
            "other values of report-type")
    if request.parameters.get('reportProjectType') == 'ACCOUNT' \
            and not request.parameters.get('eoAccount'):
        raise AssertionError(
            "Please, specified the \'account-id\' parameter for the "
            "ACCOUNT report-type parameter")
    request.parameters['format'] = 'EMAIL'

    return request

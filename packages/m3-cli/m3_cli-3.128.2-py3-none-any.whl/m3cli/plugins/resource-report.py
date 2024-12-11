"""
The custom logic for the command m3 report.
This logic is created to convert parameters from the Human readable format to
appropriate for M3 SDK API request.
"""
import json

from m3cli.plugins.utils.plugin_utilities import processing_report_format
from m3cli.utils.utilities import timestamp_to_iso


def create_custom_request(request):
    """ Transform 'resource-report' command parameters from the Human
    readable format to appropriate for M3 SDK API request.

    :param request: Dictionary with command name, api action, method and
    parameters
    :type request: BaseRequest
    """
    processing_report_format(request)
    params = request.parameters
    from_date = params.get('from')
    to_date = params.get('to')
    if from_date >= to_date:
        raise AssertionError('Parameter "from" can not be equal or greater '
                             'than parameter "to"')
    request.parameters['target'] = {'tenantGroup': params.pop('tenantGroup'),
                                    'reportUnit': 'TENANT_GROUP'}
    target = request.parameters['target']
    if params.get('clouds') and params.get('region'):
        raise AssertionError('Parameters "clouds" and "regions" can not be'
                             ' specified together')
    elif params.get('clouds'):
        target.update({
            'reportUnit': 'TENANT_GROUP_AND_CLOUD',
            'clouds': params.pop('clouds')
        })
    elif params.get('region'):
        target.update({
            'region': params.pop('region')
        })
    return request


def create_custom_response(request, response):
    """ Transform the command 'resource-report' response from M3 SDK API
    to the more human readable format.

    :param response: Server response with data as a string representation
    of a dictionary
    """
    try:
        response = json.loads(response)
    except json.decoder.JSONDecodeError:
        return response
    response_processed = []
    grand_total = response.get('grandTotal')
    if grand_total is not None:
        for each_row in response.get('records'):
            # TODO to investigate how to replace projectCode with
            #  tenantName on api side
            project_code = each_row.get('projectCode')
            if project_code:
                each_row['tenantName'] = each_row.pop('projectCode')
            if each_row.get('billingPeriodStartDate'):
                each_row['billingPeriodStartDate'] = \
                    timestamp_to_iso(each_row.get('billingPeriodStartDate'))
            if each_row.get('billingPeriodEndDate'):
                each_row['billingPeriodEndDate'] = \
                    timestamp_to_iso(each_row.get('billingPeriodEndDate'))
            response_processed.append(each_row)
        response_processed.append({'recordType': 'grandTotal',
                                   'totalPrice': grand_total,
                                   'currencyCode': 'USD'})
        return response_processed
    if response.get('message'):
        return response.get('message')
    return response

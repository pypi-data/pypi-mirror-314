"""
Sage Intacct Invdocumententry
"""
from typing import Dict

from .api_base import ApiBase


class Invdocumententry(ApiBase):
    """Class for Contacts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='INVDOCUMENTENTRY')

    def get_all(self):
        """Get all INVDOCUMENTENTRY records from Sage Intacct

        Returns:
            List of Dict in INVDOCUMENTENTRY.
        """

        complete_data = []

        pagesize = '1000'
        data = {
            'readByQuery': {
                'object': 'INVDOCUMENTENTRY',
                'fields': '*',
                'query': None,
                'pagesize': pagesize
            }
        }
        firstResult = self.format_and_send_request(data)
        print(firstResult)
        complete_data.extend(firstResult['data']['invdocumententry'])

        numRemaining = firstResult['data']['@numremaining']
        resultId = firstResult['data']['@resultId']
        while int(numRemaining) > 0:
            data = {
                'readMore': {
                    'resultId': resultId
                }
            }
            nextResult = self.format_and_send_request(data)
            complete_data.extend(nextResult['data']['invdocumententry'])
            numRemaining = nextResult['data']['@numremaining']
            resultId = nextResult['data']['@resultId']

        return complete_data

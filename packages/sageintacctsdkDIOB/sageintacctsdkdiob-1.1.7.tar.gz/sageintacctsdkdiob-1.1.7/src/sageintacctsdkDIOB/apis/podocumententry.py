"""
Sage Intacct Podocumententry
"""
from typing import Dict

from .api_base import ApiBase


class Podocumententry(ApiBase):
    """Class for Contacts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='PODOCUMENTENTRY')

    def get_all(self):
        """Get all PODOCUMENTENTRY records from Sage Intacct

        Returns:
            List of Dict in PODOCUMENTENTRY.
        """

        complete_data = []

        pagesize = '1000'
        data = {
            'readByQuery': {
                'object': 'PODOCUMENTENTRY',
                'fields': '*',
                'query': None,
                'pagesize': pagesize,
            }
        }
        firstResult = self.format_and_send_request(data)
        complete_data.extend(firstResult['data']['podocumententry'])

        numRemaining = firstResult['data']['@numremaining']
        resultId = firstResult['data']['@resultId']
        while int(numRemaining) > 0:
            data = {
                'readMore': {
                    'resultId': resultId
                }
            }
            nextResult = self.format_and_send_request(data)
            complete_data.extend(nextResult['data']['podocumententry'])
            numRemaining = nextResult['data']['@numremaining']
            resultId = nextResult['data']['@resultId']

        return complete_data

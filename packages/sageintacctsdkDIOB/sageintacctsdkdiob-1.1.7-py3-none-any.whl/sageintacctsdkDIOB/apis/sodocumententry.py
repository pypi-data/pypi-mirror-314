"""
Sage Intacct Sodocumententry
"""
from typing import Dict

from .api_base import ApiBase


class Sodocumententry(ApiBase):
    """Class for Contacts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='SODOCUMENTENTRY')

    def get_all(self):
        """Get all SODOCUMENTENTRY records from Sage Intacct

        Returns:
            List of Dict in SODOCUMENTENTRY.
        """

        complete_data = []

        pagesize = '1000'
        data = {
            'readByQuery': {
                'object': 'SODOCUMENTENTRY',
                'fields': '*',
                'query': None,
                'pagesize': pagesize,
            }
        }
        firstResult = self.format_and_send_request(data)
        complete_data.extend(firstResult['data']['sodocumententry'])

        numRemaining = firstResult['data']['@numremaining']
        resultId = firstResult['data']['@resultId']
        while int(numRemaining) > 0:
            data = {
                'readMore': {
                    'resultId': resultId
                }
            }
            nextResult = self.format_and_send_request(data)
            complete_data.extend(nextResult['data']['sodocumententry'])
            numRemaining = nextResult['data']['@numremaining']
            resultId = nextResult['data']['@resultId']

        return complete_data

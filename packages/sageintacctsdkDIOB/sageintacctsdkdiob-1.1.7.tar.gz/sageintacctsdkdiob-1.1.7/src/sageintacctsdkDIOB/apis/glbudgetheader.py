"""
Sage Intacct Glbudgetheader
"""
from typing import Dict

from .api_base import ApiBase


class Glbudgetheader(ApiBase):
    """Class for Contacts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='GLBUDGETHEADER')

    def get_all(self):
            """Get all GLBUDGETHEADER records from Sage Intacct

            Returns:
                List of Dict in GLBUDGETHEADER.
            """

            complete_data = []

            pagesize = '1000'
            data = {
                'readByQuery': {
                    'object': 'GLBUDGETHEADER',
                    'fields': '*',
                    'query': None,
                    'pagesize': pagesize,
                }
            }
            firstResult = self.format_and_send_request(data)
            complete_data.extend(firstResult['data']['glbudgetheader'])

            numRemaining = firstResult['data']['@numremaining']
            resultId = firstResult['data']['@resultId']
            while int(numRemaining) > 0:
                data = {
                    'readMore': {
                        'resultId': resultId
                    }
                }
                nextResult = self.format_and_send_request(data)
                complete_data.extend(nextResult['data']['glbudgetheader'])
                numRemaining = nextResult['data']['@numremaining']
                resultId = nextResult['data']['@resultId']

            return complete_data

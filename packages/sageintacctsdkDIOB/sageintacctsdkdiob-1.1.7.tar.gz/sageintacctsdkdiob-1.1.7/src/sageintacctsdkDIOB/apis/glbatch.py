"""
Sage Intacct Glbatch
"""
from typing import Dict

from .api_base import ApiBase


class Glbatch(ApiBase):
    """Class for Contacts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='GLBATCH')

    def get_all(self):
            """Get all GLBATCH records from Sage Intacct

            Returns:
                List of Dict in GLBATCH.
            """

            complete_data = []

            pagesize = '1000'
            data = {
                'readByQuery': {
                    'object': 'GLBATCH',
                    'fields': '*',
                    'query': None,
                    'pagesize': pagesize,
                }
            }
            firstResult = self.format_and_send_request(data)
            complete_data.extend(firstResult['data']['glbatch'])

            numRemaining = firstResult['data']['@numremaining']
            resultId = firstResult['data']['@resultId']
            while int(numRemaining) > 0:
                data = {
                    'readMore': {
                        'resultId': resultId
                    }
                }
                nextResult = self.format_and_send_request(data)
                complete_data.extend(nextResult['data']['glbatch'])
                numRemaining = nextResult['data']['@numremaining']
                resultId = nextResult['data']['@resultId']

            return complete_data

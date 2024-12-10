"""
Sage Intacct items
"""
from typing import Dict

from .api_base import ApiBase


class Items(ApiBase):
    """Class for Items APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='ITEM')

    def get_all(self):
            """Get all ITEM records from Sage Intacct

            Returns:
                List of Dict in ITEM.
            """

            complete_data = []

            pagesize = '1000'
            data = {
                'readByQuery': {
                    'object': 'ITEM',
                    'fields': '*',
                    'query': None,
                    'pagesize': pagesize,
                }
            }
            firstResult = self.format_and_send_request(data)
            complete_data.extend(firstResult['data']['item'])

            numRemaining = firstResult['data']['@numremaining']
            resultId = firstResult['data']['@resultId']
            while int(numRemaining) > 0:
                data = {
                    'readMore': {
                        'resultId': resultId
                    }
                }
                nextResult = self.format_and_send_request(data)
                complete_data.extend(nextResult['data']['item'])
                numRemaining = nextResult['data']['@numremaining']
                resultId = nextResult['data']['@resultId']

            return complete_data

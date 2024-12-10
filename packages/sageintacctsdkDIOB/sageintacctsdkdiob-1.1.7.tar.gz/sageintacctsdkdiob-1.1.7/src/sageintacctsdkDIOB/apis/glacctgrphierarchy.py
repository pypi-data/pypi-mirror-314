"""
Sage Intacct Glacctgrphierarchy
"""
from typing import Dict

from .api_base import ApiBase


class Glacctgrphierarchy(ApiBase):
    """Class for Contacts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='GLACCTGRPHIERARCHY')

    def get_all(self):
            """Get all GLACCTGRPHIERARCHY records from Sage Intacct

            Returns:
                List of Dict in GLACCTGRPHIERARCHY.
            """

            complete_data = []

            pagesize = '1000'
            data = {
                'readByQuery': {
                    'object': 'GLACCTGRPHIERARCHY',
                    'fields': '*',
                    'query': None,
                    'pagesize': pagesize,
                }
            }
            firstResult = self.format_and_send_request(data)
            complete_data.extend(firstResult['data']['glacctgrphierarchy'])

            numRemaining = firstResult['data']['@numremaining']
            resultId = firstResult['data']['@resultId']
            while int(numRemaining) > 0:
                data = {
                    'readMore': {
                        'resultId': resultId
                    }
                }
                nextResult = self.format_and_send_request(data)
                complete_data.extend(nextResult['data']['glacctgrphierarchy'])
                numRemaining = nextResult['data']['@numremaining']
                resultId = nextResult['data']['@resultId']

            return complete_data

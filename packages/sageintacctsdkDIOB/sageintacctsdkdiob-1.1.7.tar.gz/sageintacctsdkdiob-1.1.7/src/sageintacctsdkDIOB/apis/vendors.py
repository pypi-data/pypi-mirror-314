"""
Sage Intacct vendors
"""
from typing import Dict

from .api_base import ApiBase
from .constants import dimensions_fields_mapping


class Vendors(ApiBase):
    """Class for Vendors APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='VENDOR')

    def get_all(self):
            """Get all VENDOR records from Sage Intacct

            Returns:
                List of Dict in VENDOR.
            """

            complete_data = []

            pagesize = '1000'
            data = {
                'readByQuery': {
                    'object': 'VENDOR',
                    'fields': '*',
                    'query': None,
                    'pagesize': pagesize,
                }
            }
            firstResult = self.format_and_send_request(data)
            complete_data.extend(firstResult['data']['vendor'])

            numRemaining = firstResult['data']['@numremaining']
            resultId = firstResult['data']['@resultId']
            while int(numRemaining) > 0:
                data = {
                    'readMore': {
                        'resultId': resultId
                    }
                }
                nextResult = self.format_and_send_request(data)
                complete_data.extend(nextResult['data']['vendor'])
                numRemaining = nextResult['data']['@numremaining']
                resultId = nextResult['data']['@resultId']

            return complete_data
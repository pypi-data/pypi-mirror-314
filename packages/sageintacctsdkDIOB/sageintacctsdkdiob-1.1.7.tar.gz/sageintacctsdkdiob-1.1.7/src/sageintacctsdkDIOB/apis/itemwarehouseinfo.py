"""
Sage Intacct Itemwarehouseinfo
"""
from typing import Dict

from .api_base import ApiBase


class Itemwarehouseinfo(ApiBase):
    """Class for Contacts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='ITEMWAREHOUSEINFO')

    def get_all(self):
        """Get all ITEMWAREHOUSEINFO records from Sage Intacct

        Returns:
            List of Dict in ITEMWAREHOUSEINFO.
        """

        complete_data = []

        pagesize = '1000'
        data = {
            'readByQuery': {
                'object': 'ITEMWAREHOUSEINFO',
                'fields': '*',
                'query': None,
                'pagesize': pagesize,
            }
        }
        firstResult = self.format_and_send_request(data)
        complete_data.extend(firstResult['data']['itemwarehouseinfo'])

        numRemaining = firstResult['data']['@numremaining']
        resultId = firstResult['data']['@resultId']
        while int(numRemaining) > 0:
            data = {
                'readMore': {
                    'resultId': resultId
                }
            }
            nextResult = self.format_and_send_request(data)
            complete_data.extend(nextResult['data']['itemwarehouseinfo'])
            numRemaining = nextResult['data']['@numremaining']
            resultId = nextResult['data']['@resultId']

        return complete_data

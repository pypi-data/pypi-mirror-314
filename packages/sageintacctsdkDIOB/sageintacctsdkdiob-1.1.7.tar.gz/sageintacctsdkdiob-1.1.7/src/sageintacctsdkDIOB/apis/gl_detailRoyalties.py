"""
Sage Intacct GL Detail 
"""
from typing import Dict

from .api_base import ApiBase

class GLDetailRoyalties(ApiBase):
    """Class for GL Detail APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='GLDETAIL')

    def get_all(self):
        """Get all GLDETAIL Royalties records from Sage Intacct

        Returns:
            List of Dict in GLDETAIL.
        """

        complete_data = []

        pagesize = '1000'
        data = {
            'readByQuery': {
                'object': 'GLDETAIL',
                'fields': '*',
                'query': 'ACCOUNTNO = 1000',
                'pagesize': pagesize,
            }
        }
        firstResult = self.format_and_send_request(data)
        complete_data.extend(firstResult['data']['gldetail'])

        numRemaining = firstResult['data']['@numremaining']
        resultId = firstResult['data']['@resultId']
        while int(numRemaining) > 0:
            data = {
                'readMore': {
                    'resultId': resultId
                }
            }
            nextResult = self.format_and_send_request(data)
            complete_data.extend(nextResult['data']['gldetail'])
            numRemaining = nextResult['data']['@numremaining']
            resultId = nextResult['data']['@resultId']

        return complete_data

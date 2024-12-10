"""
Sage Intacct customer
"""
from .api_base import ApiBase


class Customers(ApiBase):
    """Class for Customers APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='CUSTOMER')

    def get_all(self):
            """Get all CUSTOMER records from Sage Intacct

            Returns:
                List of Dict in CUSTOMER.
            """

            complete_data = []

            pagesize = '1000'
            data = {
                'readByQuery': {
                    'object': 'CUSTOMER',
                    'fields': '*',
                    'query': 'STORE_ID > 0',
                    'pagesize': pagesize,
                }
            }
            firstResult = self.format_and_send_request(data)
            complete_data.extend(firstResult['data']['customer'])

            numRemaining = firstResult['data']['@numremaining']
            resultId = firstResult['data']['@resultId']
            while int(numRemaining) > 0:
                data = {
                    'readMore': {
                        'resultId': resultId
                    }
                }
                nextResult = self.format_and_send_request(data)
                complete_data.extend(nextResult['data']['customer'])
                numRemaining = nextResult['data']['@numremaining']
                resultId = nextResult['data']['@resultId']

            return complete_data

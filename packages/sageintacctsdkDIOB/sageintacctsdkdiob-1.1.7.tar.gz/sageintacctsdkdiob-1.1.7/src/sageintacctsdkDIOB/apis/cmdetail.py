"""
Sage Intacct charge card Cmdetail
"""
from typing import Dict

from .api_base import ApiBase


class Cmdetail(ApiBase):
    """Class for Charge Card Accounts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='CMDETAIL')

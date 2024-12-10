"""
Sage Intacct charge card Cmrecord
"""
from typing import Dict

from .api_base import ApiBase


class Cmrecord(ApiBase):
    """Class for Charge Card Accounts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='CMRECORD')

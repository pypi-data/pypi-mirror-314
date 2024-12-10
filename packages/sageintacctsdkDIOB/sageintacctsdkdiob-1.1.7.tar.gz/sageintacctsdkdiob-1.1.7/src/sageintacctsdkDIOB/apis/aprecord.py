"""
Sage Intacct charge card Aprecord
"""
from typing import Dict

from .api_base import ApiBase


class Aprecord(ApiBase):
    """Class for Charge Card Accounts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='APRECORD')

"""
Sage Intacct charge card Apdetail
"""
from typing import Dict

from .api_base import ApiBase


class Apdetail(ApiBase):
    """Class for Charge Card Accounts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='APDETAIL')

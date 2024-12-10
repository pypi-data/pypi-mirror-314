"""
Sage Intacct charge card Arrecord
"""
from typing import Dict

from .api_base import ApiBase


class Arrecord(ApiBase):
    """Class for Charge Card Accounts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='ARRECORD')

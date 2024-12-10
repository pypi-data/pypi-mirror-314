"""
Sage Intacct charge card Eerecord
"""
from typing import Dict

from .api_base import ApiBase


class Eerecord(ApiBase):
    """Class for Charge Card Accounts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='EERECORD')

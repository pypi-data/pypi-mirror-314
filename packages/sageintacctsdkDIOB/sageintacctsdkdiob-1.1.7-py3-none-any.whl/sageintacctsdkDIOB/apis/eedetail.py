"""
Sage Intacct charge card Eedetail
"""
from typing import Dict

from .api_base import ApiBase


class Eedetail(ApiBase):
    """Class for Charge Card Accounts APIs."""
    def __init__(self):
        ApiBase.__init__(self, dimension='EEDETAL')

# flake8: noqa: E501
import dataclasses
import json
import logging
import requests
import time

from web3 import HTTPProvider
from web3 import Web3

from blockchains.bid import Bid

_logger = logging.getLogger(__name__)


class Pantos(object):
    pan_price_euro = 0

    def __init__(self):
        _logger.info("Entering" + __name__ + "init")

    def get_price(self):
        """ GET THE NEW DATA VIA API HIGH FREQUENCY!!!!!!"""
        try:
            """ GET THE PAN PRICE"""
            headers = {"Accept": "application/json"}
            response = requests.get(
                "https://api.onetrading.com/public/v1/market-ticker/PAN_EUR", headers=headers)
            response.raise_for_status()
            jsonResponse = response.json()
            self.pan_price_euro = float(jsonResponse["best_bid"])
            _logger.info("Current PAN price: " + str(self.pan_price_euro))
            return self.pan_price_euro
        except Exception as error:
            print(error)
            _logger.error(error)
            return 0

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


class BscBids(object):
    amount_gas: int = 141000

    local_bids = {}
    gas_price = 0
    cur_price_euro = 0

    def __init__(self):
        _logger.info("Entering" + __name__ + "init")

    def get_bids(self, dest_chain: int):
        return self.local_bids

    def calc_bids(self, pan_price_euro_if: float):
        """ OK HOW MANY PANTOS DO I REALLY NEED:"""
        panini_price_exa_euro = pan_price_euro_if * 10000000000
        trx_price_wei = self.amount_gas * self.gas_price
        trx_price_exa_euro = trx_price_wei * self.cur_price_euro
        amount_panini = trx_price_exa_euro / panini_price_exa_euro
        amount_panini = round(amount_panini)
        _logger.info("Berechnete Pan Menge: " + str(amount_panini))
        """ OK HOW MANY PANTOS WILL WE REQUEST FROM CUSTOMER:"""
        pass
        current_unix_time = int(time.time())
        valid_until = current_unix_time + 300

        bids = '{"Delay":0, "Bids": []}'
        bid1 = '{ "fee":' + self.round_panini(amount_panini*3) + \
            ',"execution_time":10, "valid_until":' + str(valid_until) + '}'
        bid2 = '{ "fee":' + self.round_panini(amount_panini*2) + \
            ',"execution_time":600, "valid_until":' + str(valid_until) + '}'
        bid3 = '{ "fee":' + self.round_panini(amount_panini*1.2) + \
            ',"execution_time":1200, "valid_until":' + str(valid_until) + '}'
        self.local_bids = json.loads(bids)
        self.local_bids["Bids"].append(bid1)
        self.local_bids["Bids"].append(bid2)
        self.local_bids["Bids"].append(bid3)
        self.local_bids["Delay"] = 60
        """-------------------------------"""

    def get_data_hf(self):
        """ GET THE NEW DATA VIA API HIGH FREQUENCY!!!!!!"""
        try:
            """ GET THE GAS PRICE"""

            url = 'https://data-seed-prebsc-1-s1.binance.org:8545/'

            web3 = Web3(HTTPProvider(url))
            self.gas_price = web3.eth.gas_price
            _logger.info("Gas price: " + str(self.gas_price))
            """ GET THE BSC PRICE"""
            headers = {"Accept": "application/json"}
            response = requests.get(
                "https://api.bitpanda.com/v1/ticker", headers=headers)
            response.raise_for_status()
            jsonResponse = response.json()
            jsonMatic = jsonResponse["BNB"]
            self.cur_price_euro = float(jsonMatic["EUR"])
            _logger.info("Price in euro: " + str(self.cur_price_euro))
        except Exception as error:
            _logger.error(error)

    def round_panini(self, panini: int):
        rnd_pan = panini / 100000000
        rnd_pan = int(round(rnd_pan))
        rnd_pan = rnd_pan * 100000000
        return str(rnd_pan)

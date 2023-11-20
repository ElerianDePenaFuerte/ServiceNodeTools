# flake8: noqa: E501
import datetime
import logging
import threading
import time

from flask import Flask, request, make_response, jsonify

from ApiProvider.RepeatedTimer import RepeatedTimer
from blockchains.avalanche import AvaxBids
from blockchains.binance import BscBids
from blockchains.enums import Blockchain
from blockchains.ethereum import EthBids
from blockchains.pantos import Pantos
from blockchains.polygon import PolyBids

_logger = logging.getLogger(__name__)


class Controller():

    def __init__(self):
        """-----Instances-----"""
        self.ethBids = None
        self.bscBids = None
        self.avaxBids = None
        self.polyBids = None
        """--------------------"""
        self.pantosCtrl = None
        self.rt_lf = None
        self.rt_hf = None
        self.panPrice = None

    def get_data_timer(self):
        _logger.info("Getting data")
        self.get_data()
        self.calc_bids()

    def start(self):
        """ Create Instances"""
        self.ethBids = EthBids()
        self.bscBids = BscBids()
        self.avaxBids = AvaxBids()
        self.polyBids = PolyBids()

        self.pantosCtrl = Pantos()
        """First round getting data"""
        self.get_data()

        """First round calculating bids"""
        self.calc_bids()

        self.rt_hf = RepeatedTimer(10, self.get_data_timer)

        app = Flask(__name__)
        app.logger.disabled = True

        @app.route("/get_bids")
        def get_bids():
            src_chain = int(request.args.get('src'))
            dest_chain = int(request.args.get('dest'))
            match src_chain:
                case Blockchain.ETHEREUM:
                    response = jsonify(self.ethBids.get_bids(dest_chain))
                    response.status_code = 200
                    response.headers["Content-Type"] = "application/json; charset=utf-8"
                    _logger.info("Response eth: " +
                                 str(self.ethBids.get_bids(dest_chain)))
                    return response
                case Blockchain.BNB_CHAIN:
                    response = jsonify(self.bscBids.get_bids(dest_chain))
                    response.status_code = 200
                    response.headers["Content-Type"] = "application/json; charset=utf-8"
                    _logger.info("Response bnb: " +
                                 str(self.ethBids.get_bids(dest_chain)))
                    return response
                case Blockchain.AVALANCHE:
                    response = jsonify(self.avaxBids.get_bids(dest_chain))
                    response.status_code = 200
                    response.headers["Content-Type"] = "application/json; charset=utf-8"
                    _logger.info("Response avax: " +
                                 str(self.ethBids.get_bids(dest_chain)))
                    return response
                case Blockchain.SOLANA:
                    pass
                case Blockchain.POLYGON:
                    response = jsonify(self.polyBids.get_bids(dest_chain))
                    response.status_code = 200
                    response.headers["Content-Type"] = "application/json; charset=utf-8"
                    _logger.info("Response matic: " +
                                 str(self.ethBids.get_bids(dest_chain)))
                    return response
                case Blockchain.CRONOS:
                    pass
                case Blockchain.FANTOM:
                    pass
                case Blockchain.CELO:
                    pass

            return "Bids for transfer from " + Blockchain(int(src_chain)).name.lower() + " to " + Blockchain(int(dest_chain)).name.lower()

        @app.route("/alive")
        def alive():
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            return current_time

        app.run("127.0.0.1", 5000, False, False)

    def calc_bids(self):
        self.ethBids.calc_bids(self.panPrice)
        self.bscBids.calc_bids(self.panPrice)
        self.avaxBids.calc_bids(self.panPrice)
        self.polyBids.calc_bids(self.panPrice)

    def get_data(self):
        self.panPrice = self.pantosCtrl.get_price()

        self.ethBids.get_data_hf()
        self.bscBids.get_data_hf()
        self.avaxBids.get_data_hf()
        self.polyBids.get_data_hf()

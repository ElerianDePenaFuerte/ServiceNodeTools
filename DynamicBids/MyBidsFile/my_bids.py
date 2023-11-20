# flake8: noqa: E501
import collections.abc
import json
import logging
import requests
import typing

from common.blockchains.enums import Blockchain
from servicenode.plugins.base import Bid
from servicenode.plugins.bids import ConfigFileBidPlugin


_logger = logging.getLogger(__name__)


class DynBidPlugin(ConfigFileBidPlugin):
    '''
    classdocs
    '''

    def __init__(self):
        """Initializes the plugin.
        """
        self.config = None
        self.delay = 60

    def get_bids(
            self, source_blockchain_id: int, destination_blockchain_id: int,
            **kwargs: typing.Any) \
            -> typing.Tuple[collections.abc.Iterable[Bid], int]:
        if source_blockchain_id == Blockchain.ETHEREUM or \
                source_blockchain_id == Blockchain.BNB_CHAIN or \
                source_blockchain_id == Blockchain.AVALANCHE or \
                source_blockchain_id == Blockchain.POLYGON:
            """ GET THE NEW DATA VIA API!!!!!!"""
            try:
                headers = {'Accept': 'application/json'}
                response = requests.get(
                    "http://127.0.0.1:5000/get_bids?src=" + str(source_blockchain_id) + "&dest=" + str(destination_blockchain_id))
                print(response.status_code)
                response.raise_for_status()
                jsonResponse = response.json()
                delay = jsonResponse["Delay"]
                jsonResponse.pop("Delay")
                bids = []
                for bid in jsonResponse["Bids"]:
                    biddict = json.loads(bid)
                    bids.append(
                        Bid(biddict['fee'], biddict['execution_time'], biddict['valid_until']))
                return bids, delay
            except Exception as error:
                print(error)
                # _logger.info(error)
                # _logger.info(str(super().get_bids(
                #    source_blockchain_id, destination_blockchain_id, **kwargs)))
                return super().get_bids(source_blockchain_id, destination_blockchain_id, **kwargs)

            """-------------------------------"""
        else:
            try:
                return super().get_bids(source_blockchain_id, destination_blockchain_id, **kwargs)
            except Exception as error:
                print(error)

    def accept_bid(self, bid: Bid, **kwargs: typing.Any) -> bool:
        # Docstring inherited
        return True

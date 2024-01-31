import collections.abc
import dataclasses
import logging

from pantos.common.blockchains.enums import Blockchain
from pantos.servicenode.blockchains.factory import get_blockchain_client
from pantos.servicenode.business.base import Interactor
from pantos.servicenode.business.base import InteractorError
from pantos.servicenode.celery import celery_app as celery_app
from pantos.servicenode.configuration import get_plugin_config
from pantos.servicenode.database.access import replace_bids
from pantos.servicenode.plugins import get_bid_plugin
from pantos.servicenode.plugins.base import Bid
from pantos.servicenode.plugins.base import BidPluginError

_logger = logging.getLogger(__name__)
"""Logger for this module."""

_DEFAULT_DELAY = 60


class BidPluginInteractorError(InteractorError):
    """Exception class for all bid plugin interactor errors.

    """
    pass


class BidPluginInteractor(Interactor):
    """Interactor for handling the bid plugin operations.

    """
    def replace_bids(self, source_blockchain: Blockchain) -> int:
        """Replace the old bids with new bids given by the bid plugin.
        Additionally, the Validator fee is added to the bid fee.

        Returns
        -------
        int
            The delay in seconds until the next bid calculation.

        Raises
        ------
        BidPluginInteractorError
            If unable to replace the bids.

        """
        bid_plugin = get_bid_plugin()
        plugin_config = get_plugin_config()
        if ('bids' in plugin_config and 'arguments' in plugin_config['bids']):
            bids_arguments = plugin_config['bids']['arguments']
            bids_validator_fee_toogle = plugin_config['bids']['deduct_validator_fee']           # MODIFICATION Elerian
        else:
            bids_arguments = {}

        source_blockchain_client = get_blockchain_client(source_blockchain)
        source_blockchain_factor = \
            source_blockchain_client.get_validator_fee_factor(
                source_blockchain)
        delay = _DEFAULT_DELAY
        for destination_blockchain in Blockchain:
            _logger.debug(f'Executing bid plugin for {source_blockchain} and '
                          f'{destination_blockchain}')
            try:
                bids, delay = bid_plugin.get_bids(source_blockchain.value,                      # MODIFICATION Elerian
                                                  destination_blockchain.value,                 # MODIFICATION Elerian
                                                  **bids_arguments)                             # MODIFICATION Elerian
                
                if not bids_validator_fee_toogle:                                               # MODIFICATION Elerian: Check if toogle is true in Config File. If yes, the Validator fee is not added on top anymore.
                    destination_blockchain_factor = \
                        source_blockchain_client.get_validator_fee_factor(
                            destination_blockchain)
                    # bids, delay = bid_plugin.get_bids(source_blockchain.value,                    # MODIFICATION Elerian: moved outside the if statment since bids need to obtained in any case.
                    #                                   destination_blockchain.value,               # MODIFICATION Elerian
                    #                                   **bids_arguments)                           # MODIFICATION Elerian
                    self.__add_validator_fee(bids, source_blockchain_factor,
                                            destination_blockchain_factor)
                    
                _logger.debug(f'Saving {len(bids)} bids in database')
                bids = [dataclasses.asdict(bid) for bid in bids]
                replace_bids(source_blockchain.value,
                             destination_blockchain.value, bids)
            except BidPluginError:
                _logger.debug('unable to execute the bid plugin',
                              exc_info=True)
            except Exception:
                _logger.critical('unable to replace the bids', exc_info=True)
        return delay

    def __add_validator_fee(self, bids: collections.abc.Iterable[Bid],
                            source_blockchain_factor: int,
                            destination_blockchain_factor: int) -> None:
        """Add the validator fee to the bid.

        Raises
        ------
        BidPluginInteractorError
            If unable to add the validator fee to the bid.

        """
        total_factor = source_blockchain_factor + destination_blockchain_factor
        for bid in bids:
            bid.fee = round(
                (bid.fee * total_factor) / source_blockchain_factor)


@celery_app.task
def execute_bid_plugin(source_blockchain_id: int):
    """Celery task for executing the bid plugin.

    Parameters
    ----------
    source_blockchain_id : int
        The source blockchain for which the plugin is executed.

    """
    bid_plugin_interactor = BidPluginInteractor()
    delay = _DEFAULT_DELAY
    try:
        delay = bid_plugin_interactor.replace_bids(
            Blockchain(source_blockchain_id))
    except Exception:
        _logger.critical('unable to replace the bids', exc_info=True)
    finally:
        execute_bid_plugin.apply_async(args=[source_blockchain_id],
                                       countdown=delay)

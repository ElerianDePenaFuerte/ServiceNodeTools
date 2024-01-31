import abc
import logging

import sqlalchemy  # type: ignore

from pantos.servicenode.business.base import InteractorError
from pantos.servicenode.database import get_session
from pantos.servicenode.database.models import Transfer


_logger = logging.getLogger(__name__)
"""Logger for this module."""


class APIError(InteractorError):
    """Exception class for all bid interactor errors.

    """
    pass


class PLUGINInteractor(abc.ABC):
    """Base class for all APIs.

    """
    def PLUGIN_read_fee_sums(self) -> list[Transfer]:
        statement = sqlalchemy.select(Transfer.status_id, sqlalchemy.func.sum(Transfer.fee).label('total_fees'), sqlalchemy.func.count(Transfer.fee).label('count_transfers')).group_by(Transfer.status_id)
        with get_session() as session:
            fees = session.execute(statement).all()
            session.expunge_all()
            return list(fees)

    def PLUGIN_get_fee_sums(self) -> list[dict]:
        try:
            _logger.info('API: Reading aggregated fees from database')    
            raw_fee_sums = self.PLUGIN_read_fee_sums()  # Hier wird self verwendet, um auf die Instanzmethode zuzugreifen
            Fee_Sums=[]
            for fee in raw_fee_sums:
                Fee_Sums.append({
                    'Status ID': fee.status_id,
                    'Total Fees': int(fee.total_fees),
                    'Total Transfers': int(fee.count_transfers)                   
                })
        except Exception:
            raise APIError('unable to read Fee_Sums from database')
        return Fee_Sums
    

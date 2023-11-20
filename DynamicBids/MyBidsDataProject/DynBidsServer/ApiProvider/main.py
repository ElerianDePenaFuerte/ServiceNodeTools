# flake8: noqa: E501

import logging
import logging.handlers
import os
import sys

from ApiProvider.Controller import Controller


_logger = logging.getLogger(__name__)
# 50=Critical // 40=Error // 30=Warning // 20=Info // 10=Debug // 0=NotSet

if __name__ == '__main__':
    handler = logging.handlers.WatchedFileHandler(
        os.environ.get("LOGFILE", "../log/DynBidServer.log"))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)

    _logger.info("Application ist starting up.")
    ctrl = Controller()
    ctrl.start()

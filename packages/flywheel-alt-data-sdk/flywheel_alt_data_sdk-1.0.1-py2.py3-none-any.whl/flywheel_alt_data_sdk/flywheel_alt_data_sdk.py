from typing import List, Dict, Any
import logging

from .service.ticker_mapping import TickerMapping, TickerMappingResponse


# Set up a logger
logger = logging.getLogger("FlywheelAltDataSDK")
logger.setLevel(logging.INFO)

# Custom ANSI color codes
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"


class ColorfulFormatter(logging.Formatter):
    def __init__(self, enable_color: bool = True):
        super().__init__()
        self.enable_color = enable_color

    def format(self, record: logging.LogRecord) -> str:
        levelno = record.levelno
        if self.enable_color:
            if levelno >= logging.ERROR:
                color = RED
            elif levelno >= logging.WARNING:
                color = YELLOW
            elif levelno >= logging.INFO:
                color = GREEN
            else:
                color = CYAN
            record.msg = f"{color}{record.msg}{RESET}"
        return super().format(record)


ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Will set formatter later in class initialization depending on user's choice
logger.addHandler(ch)


class Client:
    def __init__(self, api_key: str, enable_color_logging: bool = True):
        """
        Initializes the FlywheelAltDataSDK client.

        :param api_key: The API key for authentication.
        :param enable_color_logging: If True, logs will be colorful; if False, no colors will be used.
        """
        self.api_key = api_key
        # Set the formatter now that we know if we should use color
        formatter = ColorfulFormatter(enable_color=enable_color_logging)
        for handler in logger.handlers:
            handler.setFormatter(formatter)

        logger.info("Initialized FlywheelAltDataSDK client.")

    def ticker_map(
        self, data: List[Dict[str, Any]], timeout: int = 500, interval: int = 5
    ) -> TickerMappingResponse:
        """
        Submits the ticker mapping request and polls for results until they are ready.

        :param data: A list of dictionaries containing brand, category, and email information.
        :param timeout: The maximum time to wait for results to be ready.
        :param interval: The time interval between polling requests.
        :return: The TickerMappingResponse containing the results.
        """
        t = TickerMapping(api_key=self.api_key, data=data, logger=logger)
        t.submit_ticker_mapping()
        return t.get_ticker_mapping_results(timeout, interval)

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import requests
import time
import enum
import logging


class ResultStatus(enum.Enum):
    FINISHED = "FINISHED"
    PENDING = "PENDING"
    
class PublicOrPrivate(enum.Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


@dataclass
class Result:
    code: str
    currency: str
    exchange: str
    name: str
    isin: Optional[str] = None
    type: Optional[str] = None
    market_cap: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    

@dataclass
class BrandContext:
    brand: str
    email: str
    index: int
    category: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class BrandResult:
    brandContext: BrandContext
    parent_company: str
    public_or_private: PublicOrPrivate
    brand: str
    results: List[Result]
    status: ResultStatus

    def to_dict(self) -> Dict[str, Any]:
        return {
            "brandContext": self.brandContext.to_dict(),
            "parent_company": self.parent_company,
            "public_or_private": self.public_or_private.value,
            "brand": self.brand,
            "results": [result.to_dict() for result in self.results],
            "status": self.status.value,
        }


@dataclass
class TickerMappingResponse:
    tickerRunId: str
    results: List[BrandResult]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tickerRunId": self.tickerRunId,
            "results": [brand_result.to_dict() for brand_result in self.results],
        }

    def json(self, pretty=True) -> str:
        return json.dumps(self.to_dict(), indent=4 if pretty else None)


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
        self.base_url = "https://api.ad.flywheeldigital.com/ticker-mapping/"
        # Set the formatter now that we know if we should use color
        formatter = ColorfulFormatter(enable_color=enable_color_logging)
        for handler in logger.handlers:
            handler.setFormatter(formatter)

        logger.info("Initialized FlywheelAltDataSDK client.")

    def _submit_ticker_mapping(self, data: List[Dict[str, Any]]) -> str:
        """
        Submits the ticker mapping request.

        :param data: A list of dictionaries containing brand, category, and email information.
        :return: The tickerRunId of the submitted request.
        :raises ValueError: If the response does not contain 'tickerRunId'.
        :raises requests.RequestException: If the request fails.
        """
        logger.debug("Submitting ticker mapping request...")
        headers = {"x-api-key": self.api_key}
        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        logger.debug(f"Received response: {result}")

        ticker_run_id = result.get("tickerRunId")
        if not ticker_run_id:
            logger.error("Response JSON does not contain 'tickerRunId'.")
            raise ValueError("Response JSON does not contain 'tickerRunId'.")

        logger.info(
            f"Submitted ticker mapping request successfully. tickerRunId: {ticker_run_id}"
        )
        return ticker_run_id

    def get_ticker_mapping_results(
        self, ticker_run_id: str, timeout: int = 500, interval: int = 5
    ) -> TickerMappingResponse:
        logger.debug(
            f"Fetching ticker mapping results for tickerRunId: {ticker_run_id}"
        )
        url = f"{self.base_url}{ticker_run_id}"
        headers = {"x-api-key": self.api_key}
        start_time = time.time()

        while True:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            response_json = response.json()
            logger.debug(f"Polled response: {response_json}")

            if all(
                brand_result["status"] == ResultStatus.FINISHED.value
                for brand_result in response_json.get("results", [])
            ):
                logger.info("All brand results finished. Returning final response.")
                return TickerMappingResponse(
                    tickerRunId=response_json["tickerRunId"],
                    results=[
                        BrandResult(
                            brandContext=BrandContext(**brand_result["brandContext"]),
                            parent_company=brand_result["parent_company"],
                            public_or_private=PublicOrPrivate(brand_result["public_or_private"].upper()),
                            brand=brand_result["brand"],
                            status=ResultStatus(brand_result["status"]),
                            results=[
                                Result(**result)
                                for result in (brand_result.get("results") or [])
                            ],
                        )
                        for brand_result in response_json["results"]
                    ],
                )

            if time.time() - start_time > timeout:
                logger.warning(
                    "Timeout reached while waiting for 'parent_company' in the response."
                )
                raise TimeoutError(
                    "Timeout reached while waiting for 'parent_company' in the response."
                )

            logger.info(
                f"Results not finished yet, waiting {interval} seconds before next poll..."
            )
            time.sleep(interval)
    
    def ticker_map(self, data: List[Dict[str, Any]], timeout: int = 500, interval: int = 5) -> TickerMappingResponse:
        """
        Submits the ticker mapping request and polls for results until they are ready.

        :param data: A list of dictionaries containing brand, category, and email information.
        :param timeout: The maximum time to wait for results to be ready.
        :param interval: The time interval between polling requests.
        :return: The TickerMappingResponse containing the results.
        """
        ticker_run_id = self._submit_ticker_mapping(data)
        return self.get_ticker_mapping_results(ticker_run_id, timeout, interval)

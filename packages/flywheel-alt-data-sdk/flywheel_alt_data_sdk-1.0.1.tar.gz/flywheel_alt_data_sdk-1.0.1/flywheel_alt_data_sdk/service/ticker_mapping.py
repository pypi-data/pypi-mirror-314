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

class TickerMapping:
    def __init__(self, api_key: str, data: List[Dict[str, Any]], logger: logging.Logger):
        """
        Initializes the TickerMapping class.

        :param api_key: The API key for authentication.
        :param data: A list of dictionaries containing brand, category, and email information.
        :param logger: The logger to use for logging.
        """

        self.api_key = api_key
        self.base_url = "https://api.ad.flywheeldigital.com/ticker-mapping/"
        self.data = data
        self.logger = logger
        self.ticker_run_id = None

    def submit_ticker_mapping(self) -> str:
        """
        Submits the ticker mapping request.

        :param data: A list of dictionaries containing brand, category, and email information.
        :return: The tickerRunId of the submitted request.
        :raises ValueError: If the response does not contain 'tickerRunId'.
        :raises requests.RequestException: If the request fails.
        """
        self.logger.debug("Submitting ticker mapping request...")
        headers = {"x-api-key": self.api_key}
        response = requests.post(self.base_url, headers=headers, json=self.data)
        response.raise_for_status()

        result = response.json()
        self.logger.debug(f"Received response: {result}")

        self.ticker_run_id = result.get("tickerRunId")
        if not self.ticker_run_id:
            self.logger.error("Response JSON does not contain 'tickerRunId'.")
            raise ValueError("Response JSON does not contain 'tickerRunId'.")

        self.logger.info(
            f"Submitted ticker mapping request successfully. tickerRunId: {self.ticker_run_id}"
        )
        return self.ticker_run_id

    def get_ticker_mapping_results(
        self, timeout: int = 500, interval: int = 5
    ) -> TickerMappingResponse:
        self.logger.debug(
            f"Fetching ticker mapping results for tickerRunId: {self.ticker_run_id}"
        )
        url = f"{self.base_url}{self.ticker_run_id}"
        headers = {"x-api-key": self.api_key}
        start_time = time.time()

        while True:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            response_json = response.json()
            self.logger.debug(f"Polled response: {response_json}")

            if all(
                brand_result["status"] == ResultStatus.FINISHED.value
                for brand_result in response_json.get("results", [])
            ):
                self.logger.info("All brand results finished. Returning final response.")
                return TickerMappingResponse(
                    tickerRunId=response_json["tickerRunId"],
                    results=[
                        BrandResult(
                            brandContext=BrandContext(**brand_result["brandContext"]),
                            parent_company=brand_result["parent_company"],
                            public_or_private=PublicOrPrivate(
                                brand_result["public_or_private"].upper()
                            ),
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
                self.logger.warning(
                    "Timeout reached while waiting for 'parent_company' in the response."
                )
                raise TimeoutError(
                    "Timeout reached while waiting for 'parent_company' in the response."
                )

            self.logger.info(
                f"Results not finished yet, waiting {interval} seconds before next poll..."
            )
            time.sleep(interval)
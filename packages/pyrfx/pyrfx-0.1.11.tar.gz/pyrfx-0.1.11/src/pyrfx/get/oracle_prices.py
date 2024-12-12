import logging
from logging import Logger
from typing import Any

import requests
from requests import Response

from pyrfx.config_manager import ConfigManager


class OraclePrices:
    """
    A class to fetch and process the latest signed prices from the RFX API for various blockchain networks.
    """

    def __init__(self, config: ConfigManager, log_level: int = logging.INFO) -> None:
        """
        Initialize the OraclePrices class with the chain name and set the API URLs.

        :param config: ConfigManager object containing chain configuration.
        :param log_level: Logging level for this class.
        """
        self.config: ConfigManager = config

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

    def get_recent_prices(self) -> dict[str, dict[str, Any]]:
        """
        Retrieve the latest signed prices from the RFX API.

        :return: A dictionary with token addresses as keys and their respective price information.
        """
        try:
            response: Response = self._make_query()
            # Ensure the request was successful
            response.raise_for_status()
            raw_output = response.json()
            # TODO: Check return data type: dict[str, dict[str, int]]
            return self._process_output(raw_output)
        except requests.RequestException as e:
            self.logger.error(f"Failed to retrieve recent prices: {e}")
            return {}
        except ValueError as e:
            self.logger.error(f"Error processing API response: {e}")
            return {}

    def _make_query(self) -> Response:
        """
        Make a GET request to the oracle URL for the specified chain.

        :return: The raw request response.
        :raises: requests.RequestException if the request fails.
        """
        self.logger.info(f"Making request to {self.config.oracle_url}")
        # Added timeout to avoid long waits
        return requests.get(self.config.oracle_url, timeout=10)

    def _process_output(self, output: dict[str, Any]) -> dict[str, Any]:
        """
        Process the API response to create a dictionary with token addresses as keys.

        :param output: The raw API response as a dictionary.
        :return: A processed dictionary where token addresses are keys, and price data is the value.
        """
        if "signedPrices" not in output:
            self.logger.error("Invalid API response structure: 'signedPrices' key not found.")
            return {}

        processed: dict[str, Any] = {item["tokenAddress"]: item for item in output["signedPrices"]}
        self.logger.info(f"Processed {len(processed)} token prices.")
        return processed

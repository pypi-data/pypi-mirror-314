import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any
from eth_typing import ChecksumAddress
from pyrfx.config_manager import ConfigManager
from pyrfx.get.data import Data
from pyrfx.get.open_interest import OpenInterest
from pyrfx.utils import execute_threading, get_funding_factor_per_period


class FundingAPR(Data):
    """
    A class that calculates funding APRs for long and short positions in RFX markets.
    It retrieves necessary data from either a local datastore or an API and performs calculations.
    """

    def __init__(self, config: ConfigManager, use_local_datastore: bool = False, log_level: int = logging.INFO) -> None:
        """
        Initialize the FundingAPR class.

        :param config: ConfigManager object containing chain configuration.
        :param use_local_datastore: Whether to use the local datastore for processing.
        :param log_level: Logging level for this class (default: logging.INFO).
        """
        super().__init__(config=config, log_level=log_level)

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.use_local_datastore: bool = use_local_datastore

    def _get_data_processing(self) -> dict[str, Any]:
        """
        Generate a dictionary of funding APR data.

        :return: Dictionary containing funding data.
        """
        open_interest = self._load_open_interest_data()

        self.logger.info("Processing RFX funding rates (% per hour) ...")

        # Lists for multithreaded execution
        mapper: list[str] = []
        output_list: list[Any] = []
        long_interest_usd_list: list[int] = []
        short_interest_usd_list: list[int] = []

        # Loop through each market and gather required data
        for market_key in self.markets.data:
            self._process_market_key(
                market_key, open_interest, output_list, long_interest_usd_list, short_interest_usd_list, mapper
            )

        # Multithreaded call on contract
        threaded_output: list[Any] = execute_threading(output_list)

        # Process the threaded output to calculate funding fees
        self._process_threaded_output(threaded_output, long_interest_usd_list, short_interest_usd_list, mapper)

        self.output["parameter"] = "funding_apr"
        return self.output

    def _load_open_interest_data(self) -> dict[str, Any]:
        """
        Load open interest data from local datastore or API.

        :return: Open interest data as a dictionary.
        """
        if self.use_local_datastore:
            open_interest_file: Path = self.config.data_path / f"{self.config.chain}_open_interest.json"
            self.logger.info(f"Loading open interest data from {open_interest_file}")
            try:
                # Use Path.read_text() to read the file content
                return json.loads(open_interest_file.read_text())
            except FileNotFoundError as e:
                self.logger.error(f"Open interest file not found: {e}")
                raise FileNotFoundError(f"Open interest file not found: {e}")
        else:
            self.logger.info("Fetching open interest data from API")
            return OpenInterest(config=self.config).get_data()

    def _process_market_key(
        self,
        market_address: ChecksumAddress,
        open_interest: dict[str, Any],
        output_list: list[Any],
        long_interest_usd_list: list[float],
        short_interest_usd_list: list[float],
        mapper: list[str],
    ) -> None:
        """
        Process each market key and gather relevant data.

        :param market_address: The market address being processed.
        :param open_interest: Open interest data.
        :param output_list: List to store market contract outputs for threading.
        :param long_interest_usd_list: List to store long interest in USD.
        :param short_interest_usd_list: List to store short interest in USD.
        :param mapper: List to store market symbols for later mapping.
        """
        try:
            symbol: str = self.markets.get_market_symbol(market_address)
            index_token_address: ChecksumAddress = self.markets.get_index_token_address(market_address)
            self._get_token_addresses(market_address=market_address)

            # Fetch oracle prices and append results to output list for threading
            output = self._get_oracle_prices(market_address, index_token_address)
            output_list.append(output)

            # Append long and short interest in USD
            long_interest_usd_list.append(open_interest["long"][symbol]["value"] * 10**30)
            short_interest_usd_list.append(open_interest["short"][symbol]["value"] * 10**30)
            mapper.append(symbol)
        except KeyError as e:
            self.logger.error(f"Error processing market {market_address}: {e}")
            raise

    def _process_threaded_output(
        self,
        threaded_output: list[Any],
        long_interest_usd_list: list[int],
        short_interest_usd_list: list[int],
        mapper: list[str],
    ) -> None:
        """
        Process the threaded output and calculate funding fees.

        :param threaded_output: Output from the multithreaded function calls.
        :param long_interest_usd_list: List of long interest USD values.
        :param short_interest_usd_list: List of short interest USD values.
        :param mapper: List of market symbols.
        """
        for output, long_interest_usd, short_interest_usd, symbol in zip(
            threaded_output, long_interest_usd_list, short_interest_usd_list, mapper
        ):
            # Market info dictionary
            market_info_dict: dict = {
                "market_token": output[0][0],
                "index_token": output[0][1],
                "long_token": output[0][2],
                "short_token": output[0][3],
                "long_borrow_fee": output[1],
                "short_borrow_fee": output[2],
                "is_long_pays_short": output[4][0],
                "funding_factor_per_second": output[4][1],
            }

            # Calculate funding fees for long and short positions
            self.output["long"][symbol] = get_funding_factor_per_period(
                market_info=market_info_dict,
                is_long=True,
                period_in_seconds=3600,
                long_interest_usd=long_interest_usd,
                short_interest_usd=short_interest_usd,
            )
            self.output["short"][symbol] = get_funding_factor_per_period(
                market_info=market_info_dict,
                is_long=False,
                period_in_seconds=3600,
                long_interest_usd=long_interest_usd,
                short_interest_usd=short_interest_usd,
            )

            self.logger.info(f"{symbol:<25} -  LONG funding hourly APR: {self.output['long'][symbol]:9.6f}%")
            self.logger.info(f"{symbol:<25} - SHORT funding hourly APR: {self.output['short'][symbol]:9.6f}%")

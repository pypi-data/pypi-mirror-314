import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any

from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.data import Data
from pyrfx.get.open_interest import OpenInterest
from pyrfx.utils import execute_threading

# from pyrfx.utils import get_funding_factor_per_period


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
        open_interest: dict[str, Any] = self._load_open_interest_data()

        self.logger.info("Processing RFX funding rates (% per hour) ...")

        # Lists for multithreaded execution
        mapper: list[str] = []
        output_list: list[Any] = []
        long_interest_usd_list: list[int] = []
        short_interest_usd_list: list[int] = []

        # Loop through each market and gather required data
        for market_address in self.markets.data:
            self._process_market(
                market_address=market_address,
                open_interest=open_interest,
                output_list=output_list,
                long_interest_usd_list=long_interest_usd_list,
                short_interest_usd_list=short_interest_usd_list,
                mapper=mapper,
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

    def _process_market(
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
            symbol: str = self.markets.get_market_symbol(market_address=market_address)
            index_token_address: ChecksumAddress = self.markets.get_index_token_address(market_address=market_address)

            # Fetch oracle prices and append results to output list for threading
            long_token_address, short_token_address = self._get_token_addresses(market_address=market_address)
            oracle_prices: tuple = self._get_oracle_prices(
                market_address=market_address,
                index_token_address=index_token_address,
                long_token_address=long_token_address,
                short_token_address=short_token_address,
                return_tuple=False,
            )
            output_list.append(oracle_prices)

            # Append long and short interest in USD
            long_interest_usd_list.append(open_interest["long"][symbol]["value"])
            short_interest_usd_list.append(open_interest["short"][symbol]["value"])
            mapper.append(symbol)
        except KeyError as e:
            self.logger.error(f"Error processing market {market_address}: {e}")
            raise

    @staticmethod
    def _get_funding_factor_per_period(
        market_info: dict, is_long: bool, period_in_seconds: int, long_interest_usd: int, short_interest_usd: int
    ) -> float:
        """
        Calculate the funding factor for a given period in a market.

        :param market_info: Dictionary of market parameters returned from the reader contract.
        :param is_long: Boolean indicating the direction of the position (long or short).
        :param period_in_seconds: The period in seconds over which to calculate the funding factor.
        :param long_interest_usd: Long interest in expanded decimals.
        :param short_interest_usd: Short interest in expanded decimals.
        :return: The funding factor for the specified period.
        """
        funding_factor_per_second = market_info["funding_factor_per_second"] / 1e28
        long_pays_shorts = market_info["is_long_pays_short"]

        is_larger_side = long_pays_shorts if is_long else not long_pays_shorts

        if is_larger_side:
            return -funding_factor_per_second * period_in_seconds

        larger_interest_usd = long_interest_usd if long_pays_shorts else short_interest_usd
        smaller_interest_usd = short_interest_usd if long_pays_shorts else long_interest_usd

        ratio = (larger_interest_usd * 10**30) / smaller_interest_usd if smaller_interest_usd > 0 else 0
        return ((ratio * funding_factor_per_second) / 10**30) * period_in_seconds

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
            market_info: dict = {
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
            self.output["long"][symbol] = self._get_funding_factor_per_period(
                market_info=market_info,
                is_long=True,
                period_in_seconds=3600,
                long_interest_usd=long_interest_usd,
                short_interest_usd=short_interest_usd,
            )
            self.output["short"][symbol] = self._get_funding_factor_per_period(
                market_info=market_info,
                is_long=False,
                period_in_seconds=3600,
                long_interest_usd=long_interest_usd,
                short_interest_usd=short_interest_usd,
            )

            self.logger.info(f"{symbol:<25} -  LONG funding hourly APR: {self.output['long'][symbol]:9.6f}%")
            self.logger.info(f"{symbol:<25} - SHORT funding hourly APR: {self.output['short'][symbol]:9.6f}%")

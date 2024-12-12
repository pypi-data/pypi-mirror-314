import logging
from logging import Logger
from typing import Any

from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.data import Data
from pyrfx.utils import execute_threading


class BorrowAPR(Data):
    """
    A class that retrieves and calculates the Borrow Annual Percentage Rate (APR) for long and short positions
    across various markets on a blockchain network, utilizing parallel data processing and logging.
    """

    def __init__(self, config: ConfigManager, log_level: int = logging.INFO) -> None:
        """
        Initialize the GetBorrowAPR class, extending the GetData class.

        :param config: ConfigManager object containing the chain configuration.
        :param log_level: Logging level for the class (default: logging.INFO)
        """
        super().__init__(config=config, log_level=log_level)

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

    def _get_data_processing(self) -> dict[str, dict[str, float]]:
        """
        Generate a dictionary of borrow APR data for each market.

        This method fetches oracle prices and market data in parallel for each market,
        processes the outputs, and computes the long and short borrow APR values.

        :return: Dictionary containing long and short borrow APR for each market.
        """
        self.logger.info("Processing Borrow APR Data")

        output_list: list = []
        mapper: list[str] = []

        # Iterate through each market and fetch relevant data
        for market_address in self.markets.data:
            try:
                # Get the index token address for the market
                index_token_address: ChecksumAddress = self.markets.get_index_token_address(
                    market_address=market_address
                )

                # Get long and short token addresses
                long_token_address, short_token_address = self._get_token_addresses(market_address=market_address)

                # Fetch oracle prices
                market_info: tuple = self._get_oracle_prices(
                    market_address=market_address,
                    index_token_address=index_token_address,
                    long_token_address=long_token_address,
                    short_token_address=short_token_address,
                    return_tuple=False,
                )

                # If the output is valid, append it for further processing
                output_list.append(market_info)
                mapper.append(self.markets.get_market_symbol(market_address=market_address))

            except KeyError as e:
                self.logger.error(f"KeyError: Missing data for market {market_address}: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error processing market {market_address}: {e}")

        # Execute threading for parallel data retrieval
        threaded_output: list = execute_threading(output_list)

        # Process the threaded outputs and log results
        self._process_threaded_output(mapper, threaded_output)

        self.output["parameter"] = "borrow_apr"
        return self.output

    def _process_threaded_output(self, mapper: list[str], threaded_output: list[Any]) -> None:
        """
        Process the output from threading, calculate APR, and log results.

        :param mapper: List of market symbols.
        :param threaded_output: Output from threading execution.
        """
        for key, output in zip(mapper, threaded_output):
            try:
                # Calculate borrow APR for both long and short positions
                long_apr: float = (output[1] / 10**28) * 3600
                short_apr: float = (output[2] / 10**28) * 3600

                self.output["long"][key] = long_apr
                self.output["short"][key] = short_apr

                # Log the calculated values
                self.logger.info(f"{key:4} | Borrow Hourly Rate | Long: -{long_apr:.5f}% | Short: -{short_apr:.5f}%")

            except (IndexError, KeyError) as e:
                self.logger.error(f"Error processing market {key}: {e}")

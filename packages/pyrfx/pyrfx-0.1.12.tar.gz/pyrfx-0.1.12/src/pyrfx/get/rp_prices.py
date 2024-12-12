import logging
from logging import Logger
from typing import Any

from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.data import Data
from pyrfx.keys import KEYS
from pyrfx.utils import execute_threading, get_reader_contract, save_csv, save_json, timestamp_df


class RPPrices(Data):
    """
    A class responsible for calculating RP prices for various actions (withdrawal, deposit, trading) in the market.
    It inherits from the base GetData class and processes market prices using contract calls.
    """

    def __init__(self, config: ConfigManager, log_level: int = logging.INFO) -> None:
        """
        Initialize RPPrices class, inheriting from GetData.

        :param config: ConfigManager object containing chain configuration.
        :param log_level: Logging level for this class (default: logging.INFO).
        """
        super().__init__(config=config, log_level=log_level)

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.reader_contract = get_reader_contract(config)

    def get_price_withdraw(self) -> dict[str, Any]:
        """
        Get RP price for withdrawing from LP.

        :return: Dictionary of RP prices.
        """
        return self._process_rp_price(KEYS["MAX_PNL_FACTOR_FOR_WITHDRAWALS"])

    def get_price_deposit(self) -> dict[str, Any]:
        """
        Get RP price for depositing to LP.

        :return: Dictionary of RP prices.
        """
        return self._process_rp_price(KEYS["MAX_PNL_FACTOR_FOR_DEPOSITS"])

    def get_price_traders(self) -> dict[str, str | float]:
        """
        Get RP price for traders.

        :return: Dictionary of RP prices.
        """
        return self._process_rp_price(KEYS["MAX_PNL_FACTOR_FOR_TRADERS"])

    def _get_data_processing(self) -> dict[str, Any]:
        """
        Process and calculate RP prices for all available markets and return the results.

        :return: Dictionary containing the processed RP prices for each market.
        """
        self.logger.info("Processing RP prices for all markets.")

        output_list: list = []
        market_symbols: list[str] = []
        self._filter_swap_markets()  # Ensure swap markets are filtered out

        # Loop through all available markets and fetch necessary data
        for market_address in self.markets.data:
            market, index_token_address = self._prepare_market_data(market_address=market_address)
            long_token_address, short_token_address = self._get_token_addresses(market_address=market_address)
            oracle_prices: tuple = self._get_oracle_prices(
                market_address=market_address,
                index_token_address=index_token_address,
                long_token_address=long_token_address,
                short_token_address=short_token_address,
                return_tuple=True,
            )

            # Prepare the query to fetch RP prices
            output = self._make_market_token_price_query(
                market, oracle_prices[0], oracle_prices[1], oracle_prices[2], KEYS["MAX_PNL_FACTOR_FOR_TRADERS"]
            )
            output_list.append(output)
            market_symbols.append(self.markets.get_market_symbol(market_address))

        # Execute multithreading for price queries
        threaded_output: list = execute_threading(output_list)

        # Process the threaded output and store the RP prices
        self._process_output(threaded_output, market_symbols)

        self.output["parameter"] = "rp_prices"
        return self.output

    def _process_rp_price(self, pnl_factor_type: bytes) -> dict[str, str | float]:
        """
        Process RP pool prices for a given profit/loss factor.

        :param pnl_factor_type: Descriptor for datastore.
        :return: Dictionary of RP prices.
        """
        output_list: list[Any] = []
        market_symbols: list[str] = []
        self._filter_swap_markets()

        for market_address in self.markets.data:
            market, index_token_address = self._prepare_market_data(market_address=market_address)
            long_token_address, short_token_address = self._get_token_addresses(market_address=market_address)
            oracle_prices: tuple = self._get_oracle_prices(
                market_address=market_address,
                index_token_address=index_token_address,
                long_token_address=long_token_address,
                short_token_address=short_token_address,
                return_tuple=True,
            )

            if oracle_prices:
                output = self._make_market_token_price_query(
                    market, oracle_prices[0], oracle_prices[1], oracle_prices[2], pnl_factor_type
                )
                output_list.append(output)
                market_symbols.append(self.markets.get_market_symbol(market_address))

        # Execute multithreading
        threaded_output = execute_threading(output_list)

        # Process the results and format the output
        self._process_output(threaded_output, market_symbols)

        # Save output to JSON or CSV if specified
        self._save_output()

        return self.output

    def _prepare_market_data(self, market_address: ChecksumAddress) -> tuple[list[ChecksumAddress], ChecksumAddress]:
        """
        Prepare market data and token addresses.

        :param market_address: Address representing the market.
        :return: Market and index token address.
        """
        long_token_address, short_token_address = self._get_token_addresses(market_address=market_address)
        index_token_address: ChecksumAddress = self.markets.get_index_token_address(market_address)
        market: list[ChecksumAddress] = [
            market_address,
            index_token_address,
            long_token_address,
            short_token_address,
        ]
        return market, index_token_address

    def _process_output(self, threaded_output: list[Any], market_symbols: list[str]) -> None:
        """
        Process the threaded output and store RP prices.

        :param threaded_output: List of outputs from threading.
        :param market_symbols: List of market symbols.
        """
        for key, output in zip(market_symbols, threaded_output):
            try:
                # Convert the output to USD value
                self.output[key] = output[0] / 10**30
            except Exception as e:
                self.logger.error(f"Error processing output for {key}: {e}")

        self.output["parameter"] = "rp_prices"

        # Clean up any unneeded keys
        self.output.pop("long", None)
        self.output.pop("short", None)

    def _save_output(self) -> None:
        """
        Save the output to JSON or CSV if required.
        """
        if self.config.save_to_json:
            file_name: str = f"{self.config.chain}_rp_prices.json"
            save_json(output_data_path=self.config.data_path, file_name=file_name, data=self.output)
            self.logger.info(f"RP Prices saved to {file_name}")

        if self.config.save_to_csv:
            file_name: str = f"{self.config.chain}_rp_prices.csv"
            save_csv(output_data_path=self.config.data_path, file_name=file_name, data=timestamp_df(data=self.output))
            self.logger.info(f"RP Prices saved to {file_name}")

    def _make_market_token_price_query(
        self,
        market: list[str],
        index_price_tuple: tuple[int, int],
        long_price_tuple: tuple[int, int],
        short_price_tuple: tuple[int, int],
        pnl_factor_type: bytes,
    ) -> Any:
        """
        Query RP price from the reader contract for a given market.

        :param market: List of contract addresses representing the market.
        :param index_price_tuple: Tuple of min and max prices for index token.
        :param long_price_tuple: Tuple of min and max prices for long token.
        :param short_price_tuple: Tuple of min and max prices for short token.
        :param pnl_factor_type: PNL factor type to use in the query.
        :return: Uncalled web3 contract object.
        """
        maximise: True = True  # Maximise to take max prices into calculation
        return self.reader_contract.functions.getMarketTokenPrice(
            self.config.contracts.data_store.contract_address,
            market,
            index_price_tuple,
            long_price_tuple,
            short_price_tuple,
            pnl_factor_type,
            maximise,
        )

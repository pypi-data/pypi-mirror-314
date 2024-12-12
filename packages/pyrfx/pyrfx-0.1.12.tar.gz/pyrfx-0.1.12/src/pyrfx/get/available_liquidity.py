import logging
from logging import Logger
from typing import Any

import numpy as np
from web3.contract.contract import Contract

from pyrfx.config_manager import ConfigManager
from pyrfx.get.data import Data
from pyrfx.get.open_interest import OpenInterest
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.keys import open_interest_reserve_factor_key, pool_amount_key, reserve_factor_key
from pyrfx.utils import execute_threading, get_data_store_contract


class AvailableLiquidity(Data):
    def __init__(self, config: ConfigManager, use_local_datastore: bool = False, log_level: int = logging.INFO) -> None:
        """
        Initialize the GetAvailableLiquidity class with ConfigManager and logging setup.

        :param config: ConfigManager object containing chain-specific configuration.
        :param use_local_datastore: Whether to use the local datastore for processing.
        :param log_level: Logging level (default: logging.INFO)
        """
        super().__init__(config=config, use_local_datastore=use_local_datastore, log_level=log_level)
        self._prices: dict[str, dict[str, Any]] | None = None

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

    def _get_data_processing(self) -> dict[str, dict[str, float]]:
        """
        Process and generate the available liquidity data for each market.

        :return: Dictionary containing available long and short liquidity for each market.
        """
        self.logger.info("Processing Available Liquidity")

        open_interest: dict = OpenInterest(self.config).get_data()

        reserved_long_list, reserved_short_list, token_price_list, mapper = [], [], [], []
        long_pool_amount_list, short_pool_amount_list = [], []
        long_reserve_factor_list, short_reserve_factor_list = [], []
        long_open_interest_reserve_factor_list, short_open_interest_reserve_factor_list = [], []
        long_precision_list, short_precision_list = [], []

        # Ensure swap markets are filtered out
        self._filter_swap_markets()

        for market_address in self.markets.data:
            long_token_address, short_token_address = self._get_token_addresses(market_address=market_address)
            market_symbol: str = self.markets.get_market_symbol(market_address=market_address)

            # Get precision factors
            long_decimal_factor: int = self.markets.get_decimal_factor(
                market_address=market_address, long=True, short=False
            )
            short_decimal_factor: int = self.markets.get_decimal_factor(
                market_address=market_address, long=False, short=True
            )

            long_precision, short_precision, oracle_precision = self._get_precision_factors(
                long_decimal_factor=long_decimal_factor, short_decimal_factor=short_decimal_factor
            )

            mapper.append(market_symbol)

            # Fetch max reserved USD for long and short pools
            # Long pool:
            (long_pool_amount, long_reserve_factor, long_open_interest_reserve_factor) = self.get_max_reserved_usd(
                market=market_address, token=long_token_address, is_long=True
            )
            reserved_long_list.append(open_interest["long"][market_symbol]["value"])
            long_pool_amount_list.append(long_pool_amount)
            long_reserve_factor_list.append(long_reserve_factor)
            long_open_interest_reserve_factor_list.append(long_open_interest_reserve_factor)
            long_precision_list.append(long_precision)

            # Short pool
            (short_pool_amount, short_reserve_factor, short_open_interest_reserve_factor) = self.get_max_reserved_usd(
                market=market_address, token=short_token_address, is_long=False
            )
            reserved_short_list.append(open_interest["short"][market_symbol]["value"])
            short_pool_amount_list.append(short_pool_amount)
            short_reserve_factor_list.append(short_reserve_factor)
            short_open_interest_reserve_factor_list.append(short_open_interest_reserve_factor)
            short_precision_list.append(short_precision)

            # Calculate token price using oracle prices
            token_price: float = self._get_token_price(long_token_address, oracle_precision)
            token_price_list.append(token_price)

        long_pool_amount_output = execute_threading(long_pool_amount_list)
        short_pool_amount_output = execute_threading(short_pool_amount_list)
        long_reserve_factor_list_output = execute_threading(long_reserve_factor_list)
        short_reserve_factor_list_output = execute_threading(short_reserve_factor_list)
        long_open_interest_reserve_factor_list_output = execute_threading(long_open_interest_reserve_factor_list)
        short_open_interest_reserve_factor_list_output = execute_threading(short_open_interest_reserve_factor_list)

        # Log liquidity for each token
        for (
            long_pool_amount,
            short_pool_amount,
            long_reserve_factor,
            short_reserve_factor,
            long_open_interest_reserve_factor,
            short_open_interest_reserve_factor,
            reserved_long,
            reserved_short,
            token_price,
            token_symbol,
            long_precision,
            short_precision,
        ) in zip(
            long_pool_amount_output,
            short_pool_amount_output,
            long_reserve_factor_list_output,
            short_reserve_factor_list_output,
            long_open_interest_reserve_factor_list_output,
            short_open_interest_reserve_factor_list_output,
            reserved_long_list,
            reserved_short_list,
            token_price_list,
            mapper,
            long_precision_list,
            short_precision_list,
        ):
            self._log_liquidity(
                token_symbol,
                long_pool_amount,
                short_pool_amount,
                long_reserve_factor,
                short_reserve_factor,
                long_open_interest_reserve_factor,
                short_open_interest_reserve_factor,
                reserved_long,
                reserved_short,
                token_price,
                long_precision,
                short_precision,
            )

        self.output["parameter"] = "available_liquidity"
        return self.output

    @staticmethod
    def _get_precision_factors(long_decimal_factor: int, short_decimal_factor: int) -> tuple[int, int, int]:
        """
        Calculate the precision factors for long, short, and oracle prices.
        :param long_decimal_factor: Decimal factor for long token.
        :return: Tuple of long precision, short precision, and oracle precision.
        """
        long_precision: int = 10 ** (30 + long_decimal_factor)
        short_precision: int = 10 ** (30 + short_decimal_factor)
        oracle_precision: int = 10 ** (30 - long_decimal_factor)
        return long_precision, short_precision, oracle_precision

    def _get_token_price(self, token_address: str, oracle_precision: int) -> float:
        """
        Retrieve token price from Oracle Prices, with error handling.

        :param token_address: The address of the token to fetch prices for.
        :param oracle_precision: Precision factor for oracle prices.
        :return: The median price of the token.
        """
        if not self._prices:
            self._prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

        try:
            return float(
                np.median(
                    [
                        float(self._prices[token_address]["maxPriceFull"]) / oracle_precision,
                        float(self._prices[token_address]["minPriceFull"]) / oracle_precision,
                    ]
                )
            )
        except KeyError as e:
            self.logger.error(f"KeyError: Price data for token {token_address} is missing: {e}")
            return 0.0

    def get_max_reserved_usd(self, market: str, token: str, is_long: bool) -> tuple[int, int, int]:
        """
        Fetch max reserved USD data using Web3 contract calls with retries.

        :param market: The market contract address.
        :param token: The token contract address (long or short).
        :param is_long: Boolean to specify long or short pool.
        :return: Tuple containing pool amount, reserve factor, and open interest reserve factor.
        """
        try:
            datastore: Contract = get_data_store_contract(config=self.config)

            pool_amount_hash: bytes = pool_amount_key(market=market, token=token)
            reserve_factor_hash: bytes = reserve_factor_key(market=market, is_long=is_long)
            open_interest_reserve_factor_hash: bytes = open_interest_reserve_factor_key(market=market, is_long=is_long)

            pool_amount: int = datastore.functions.getUint(pool_amount_hash)
            reserve_factor: int = datastore.functions.getUint(reserve_factor_hash)
            open_interest_reserve_factor: int = datastore.functions.getUint(open_interest_reserve_factor_hash)

            return pool_amount, reserve_factor, open_interest_reserve_factor
        except Exception as e:
            self.logger.error(f"Error fetching max reserved USD for {market}: {e}")
            raise

    def _log_liquidity(
        self,
        token_symbol: str,
        long_pool_amount: Any,
        short_pool_amount: Any,
        long_reserve_factor: Any,
        short_reserve_factor: Any,
        long_open_interest_reserve_factor: Any,
        short_open_interest_reserve_factor: Any,
        reserved_long: Any,
        reserved_short: Any,
        token_price: float,
        long_precision: int,
        short_precision: int,
    ) -> None:
        """
        Log and compute liquidity for both long and short positions.

        :param token_symbol: Token symbol for logging.
        :param long_pool_amount: Long pool amount.
        :param short_pool_amount: Short pool amount.
        :param long_reserve_factor: Long reserve factor.
        :param short_reserve_factor: Short reserve factor.
        :param long_open_interest_reserve_factor: Long open interest reserve factor.
        :param short_open_interest_reserve_factor: Short open interest reserve factor.
        :param reserved_long: Reserved long value.
        :param reserved_short: Reserved short value.
        :param token_price: Token price from the oracle.
        :param long_precision: Long precision value.
        :param short_precision: Short precision value.
        """
        self.logger.info(f"Token: {token_symbol}")

        # Long liquidity calculation
        long_reserve_factor = min(long_reserve_factor, long_open_interest_reserve_factor)
        long_max_reserved_tokens = long_pool_amount * long_reserve_factor
        long_max_reserved_usd = (long_max_reserved_tokens / long_precision) * token_price
        long_liquidity = long_max_reserved_usd - float(reserved_long)
        self.logger.info(f"Available Long Liquidity: ${long_liquidity:,.2}")
        self.output["long"][token_symbol] = long_liquidity

        # Short liquidity calculation
        short_reserve_factor = min(short_reserve_factor, short_open_interest_reserve_factor)
        short_max_reserved_usd = (short_pool_amount * short_reserve_factor) / short_precision
        short_liquidity = short_max_reserved_usd - float(reserved_short)
        self.logger.info(f"Available Short Liquidity: ${short_liquidity:,.2}")
        self.output["short"][token_symbol] = short_liquidity

import logging
from logging import Logger
from typing import Any

import numpy as np
from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.data import Data
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.keys import claimable_fee_amount_key
from pyrfx.utils import execute_threading, get_data_store_contract


class ClaimableFees(Data):
    """
    A class that retrieves and calculates the total claimable fees (both long and short) across markets
    for a given chain, utilizing threading and logging.
    """

    def __init__(self, config: ConfigManager, log_level: int = logging.INFO) -> None:
        """
        Initialize the GetClaimableFees class, inheriting from GetData.

        :param config: ConfigManager object containing chain configuration.
        :param log_level: Logging level for this class.
        """
        super().__init__(config=config, log_level=log_level)

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self._prices: dict[str, dict[str, Any]] | None = None

    def _get_data_processing(self) -> dict[str, float]:
        """
        Get the total claimable fees in USD.

        :return: A dictionary containing total fees for the current week.
        """
        total_fees: float = 0.0
        long_output_list: list = []
        short_output_list: list = []
        long_precision_list: list = []
        long_token_price_list: list = []
        mapper: list = []

        self._filter_swap_markets()

        # Process each market and prepare data for threading
        for market_address in self.markets.data:
            self._process_market(
                market_address=market_address,
                long_output_list=long_output_list,
                short_output_list=short_output_list,
                long_precision_list=long_precision_list,
                long_token_price_list=long_token_price_list,
                mapper=mapper,
            )

        # Execute threading to process long and short fees in parallel
        long_threaded_output = execute_threading(long_output_list)
        short_threaded_output = execute_threading(short_output_list)

        # Calculate total fees and return
        total_fees: float = self._calculate_total_fees(
            long_threaded_output, short_threaded_output, long_precision_list, long_token_price_list, mapper, total_fees
        )

        return {"total_fees": total_fees, "parameter": "total_fees"}

    def _process_market(
        self,
        market_address: ChecksumAddress,
        long_output_list: list,
        short_output_list: list,
        long_precision_list: list,
        long_token_price_list: list,
        mapper: list,
    ) -> None:
        """
        Process each market key, fetch oracle prices, and prepare uncalled Web3 functions for threading.

        :param market_address: The address of the market to process.
        :param long_output_list: List to store uncalled web3 objects for long fees.
        :param short_output_list: List to store uncalled web3 objects for short fees.
        :param long_precision_list: List to store long precision values.
        :param long_token_price_list: List to store long token prices.
        :param mapper: List to store market symbols for mapping.
        """
        long_token_address, short_token_address = self._get_token_addresses(market_address=market_address)
        market_symbol: str = self.markets.get_market_symbol(market_address)
        long_decimal_factor: int = self.markets.get_decimal_factor(
            market_address=market_address, long=True, short=False
        )
        long_precision: int = 10 ** (long_decimal_factor - 1)
        oracle_precision: int = 10 ** (30 - long_decimal_factor)

        # Fetch uncalled web3 object for long fees
        long_output: Any = self._get_claimable_fee_amount(market_address, long_token_address)

        # Fetch oracle prices if not already cached
        if not self._prices:
            self._prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

        long_token_price: float = float(
            np.median(
                [
                    float(self._prices[long_token_address]["maxPriceFull"]) / oracle_precision,
                    float(self._prices[long_token_address]["minPriceFull"]) / oracle_precision,
                ]
            )
        )

        # Add relevant data to lists for threading
        long_token_price_list.append(long_token_price)
        long_precision_list.append(long_precision)
        long_output_list.append(long_output)
        short_output_list.append(self._get_claimable_fee_amount(market_address, short_token_address))
        mapper.append(market_symbol)

    def _calculate_total_fees(
        self,
        long_threaded_output: list,
        short_threaded_output: list,
        long_precision_list: list,
        long_token_price_list: list,
        mapper: list,
        total_fees: float,
    ) -> float:
        """
        Calculate the total claimable fees and log the results.

        :param long_threaded_output: List of claimable long fees from threading.
        :param short_threaded_output: List of claimable short fees from threading.
        :param long_precision_list: List of precision values for long tokens.
        :param long_token_price_list: List of prices for long tokens.
        :param mapper: List of market symbols.
        :param total_fees: Running total of the fees.
        :return: Updated total fees.
        """
        for long_claimable_fees, short_claimable_fees, long_precision, long_token_price, token_symbol in zip(
            long_threaded_output, short_threaded_output, long_precision_list, long_token_price_list, mapper
        ):
            # Convert raw outputs into USD value
            long_claimable_usd: float = (long_claimable_fees / long_precision) * long_token_price
            # TODO: Check if all short tokens / fees are in USDC ...
            short_claimable_usd: float = short_claimable_fees / (10**6)  # Short fees are in USDC (6 decimals)

            # Log results with padded token symbol (6 characters wide)
            self.logger.info(f"{token_symbol:6} - Long Claimable Fees: ${long_claimable_usd:,.2}")
            self.logger.info(f"{token_symbol:6} - Short Claimable Fees: ${short_claimable_usd:,.2}")

            # Update total fees
            total_fees += long_claimable_usd + short_claimable_usd

        return total_fees

    def _get_claimable_fee_amount(self, market_address: str, token_address: str) -> Any:
        """
        Fetch the uncalled web3 object for claimable fees from the datastore.

        :param market_address: Address of the RFX market.
        :param token_address: Address of either the long or short collateral token.
        :return: Uncalled web3 object for the claimable fee amount.
        """
        datastore = get_data_store_contract(self.config)
        claimable_fees_amount_hash_data = claimable_fee_amount_key(market_address, token_address)
        return datastore.functions.getUint(claimable_fees_amount_hash_data)

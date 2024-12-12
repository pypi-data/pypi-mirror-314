import logging
from logging import Logger
from typing import Any

import numpy as np
from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.data import Data
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import get_token_balance_contract, save_json


class ContractBalance(Data):
    """
    A class to retrieve the USD balance of contracts in liquidity pools across markets for a given blockchain network.
    Inherits from the GetData class for seamless integration into the SDK.
    """

    def __init__(self, config: ConfigManager, log_level: int = logging.INFO) -> None:
        """
        Initialize the GetContractBalance class, inheriting from GetData.

        :param config: ConfigManager object containing chain-specific configuration.
        :param log_level: Logging level for this class (default: logging.INFO).
        """
        super().__init__(config=config, log_level=log_level)

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self._prices: dict[str, dict[str, Any]] = {}

    def get_pool_balances(self) -> dict[str, dict[str, float]]:
        """
        Fetch the USD balances of each pool and optionally save them to a JSON file.

        :return: A dictionary of total USD values per pool.
        """
        self.logger.info("Fetching available markets.")
        available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(self.config).get_available_markets()
        pool_balances: dict[str, Any] = {}
        self._prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

        for market in available_markets:
            market_symbol: str = available_markets[market]["market_symbol"]
            long_token_address: str = available_markets[market]["long_token_address"]
            short_token_address: str = available_markets[market]["short_token_address"]

            # Query the token balances
            long_token_balance, short_token_balance = self._query_balances(
                market, long_token_address, short_token_address
            )

            # Calculate the USD value for the long token
            oracle_precision: int = 10 ** (30 - available_markets[market]["long_token_metadata"]["decimals"])
            long_usd_balance: float = self._calculate_usd_value(
                long_token_balance, long_token_address, oracle_precision
            )

            # Store the total TVL (Total Value Locked) and token addresses
            pool_balances[market_symbol] = {
                "total_tvl": long_usd_balance + short_token_balance,
                "long_token": long_token_address,
                "short_token": short_token_address,
            }

            self.logger.info(f"{market_symbol:4} | Pool USD Value: ${long_usd_balance + short_token_balance:,.2f}")

        if self.config.save_to_json:
            file_name: str = f"{self.config.chain}_contract_balances.json"
            save_json(
                output_data_path=self.config.data_path,
                file_name=file_name,
                data=pool_balances,
            )
            self.logger.info(f"Saved pool balances to {file_name}")

        return pool_balances

    def _query_balances(self, market: str, long_token_address: str, short_token_address: str) -> tuple[float, float]:
        """
        Query token balances for the long and short tokens in a given market.

        :param market: RFX market address.
        :param long_token_address: Address of the long token.
        :param short_token_address: Address of the short token.
        :return: A tuple containing the long token balance and short token balance.
        """
        try:
            # Get the balance for the long token
            long_token_contract = get_token_balance_contract(self.config, long_token_address)
            long_token_balance: float = (
                long_token_contract.functions.balanceOf(market).call()
                / 10 ** long_token_contract.functions.decimals().call()
            )

            # Get the balance for the short token
            short_token_contract = get_token_balance_contract(self.config, short_token_address)
            short_token_balance: float = (
                short_token_contract.functions.balanceOf(market).call()
                / 10 ** short_token_contract.functions.decimals().call()
            )

            return long_token_balance, short_token_balance

        except Exception as e:
            self.logger.error(f"Error querying token balances for market {market}: {e}")
            return 0.0, 0.0

    def _calculate_usd_value(self, token_balance: float, contract_address: str, oracle_precision: int) -> float:
        """
        Calculate the USD value for a given token balance.

        :param token_balance: Amount of tokens.
        :param contract_address: Address of the token contract.
        :param oracle_precision: Precision factor to apply to the token price.
        :return: The USD value of the tokens.
        """
        try:
            token_price: float = float(
                np.median(
                    [
                        float(self._prices[contract_address]["maxPriceFull"]) / oracle_precision,
                        float(self._prices[contract_address]["minPriceFull"]) / oracle_precision,
                    ]
                )
            )
            return token_price * token_balance
        except KeyError:
            self.logger.error(f"Contract address {contract_address} not found in oracle prices.")
            return 0.0

import logging
from logging import Logger
from typing import Any

import numpy as np
from web3.types import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.data import Data
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import get_available_tokens


class OpenPositions(Data):
    """
    A class responsible for retrieving and processing open positions for a given address on a blockchain.
    """

    def __init__(
        self, config: ConfigManager, address: ChecksumAddress | None = None, log_level: int = logging.INFO
    ) -> None:
        """
        Initialize the GetOpenPositions class with the configuration and EVM address.

        :param config: ConfigManager object containing chain configuration.
        :param address: EVM address for querying open positions.
        :param log_level: Logging level for this class.
        """
        super().__init__(config=config, log_level=log_level)
        self.address: ChecksumAddress = address if address else config.user_wallet_address
        self.chain_tokens: dict[ChecksumAddress, dict[str, ChecksumAddress | int | bool]] = get_available_tokens(
            config=config
        )

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self._raw_position: Any = None

    def get_open_positions(self) -> dict[str, Any]:
        """
        Get all open positions for the given address on the chain defined in the class init.

        :return: A dictionary containing the open positions, with asset and direction as keys.
        """
        raw_positions = self._fetch_raw_positions()

        if not raw_positions:
            self.logger.info(f'No positions open for address: "{self.address}" on {self.config.chain}.')
            return {}

        processed_positions = self._process_raw_positions(raw_positions)
        return processed_positions

    def _fetch_raw_positions(self) -> list[Any]:
        """
        Fetch raw positions data from the reader contract.

        :return: List of raw position data from the contract.
        """
        return self.reader_contract.functions.getAccountPositions(
            self.config.contracts.data_store.contract_address, self.address, 0, 2**256 - 1
        ).call()

    def _process_raw_positions(self, raw_positions: list[Any]) -> dict[str, Any]:
        """
        Process raw positions data into a structured dictionary.

        :param raw_positions: List of raw position data from the contract.
        :return: Dictionary of processed positions.
        """
        processed_positions: dict[str, Any] = {}

        for raw_position in raw_positions:
            try:
                self._raw_position: Any = raw_position
                processed_position: dict[str, Any] = self._get_data_processing()
                direction = "long" if processed_position["is_long"] else "short"
                key = f"{processed_position['market_symbol'][0]}_{direction}"
                processed_positions[key] = processed_position
            except KeyError as e:
                self.logger.error(f"Incompatible market: {e}")

        return processed_positions

    def _get_data_processing(self) -> dict[str, Any]:
        """
        Process individual raw position data into a structured dictionary.

        :return: Processed position data as a dictionary.
        """
        market_info = self.markets.data[self._raw_position[0][1]]
        entry_price, leverage, mark_price = self._calculate_position_metrics(self._raw_position, market_info)

        return {
            "account": self._raw_position[0][0],
            "market": self._raw_position[0][1],
            "market_symbol": (market_info["market_symbol"],),
            "collateral_token": self.chain_tokens[self._raw_position[0][2]]["symbol"],
            "position_size": self._raw_position[1][0] / 10**30,
            "size_in_tokens": self._raw_position[1][1],
            "entry_price": entry_price,
            "initial_collateral_amount": self._raw_position[1][2],
            "initial_collateral_amount_usd": self._raw_position[1][2]
            / 10 ** self.chain_tokens[self._raw_position[0][2]]["decimals"],
            "leverage": leverage,
            "borrowing_factor": self._raw_position[1][3],
            "funding_fee_amount_per_size": self._raw_position[1][4],
            "long_token_claimable_funding_amount_per_size": self._raw_position[1][5],
            "short_token_claimable_funding_amount_per_size": self._raw_position[1][6],
            "position_modified_at": "",  # Placeholder for modification time if needed
            "is_long": self._raw_position[2][0],
            "percent_profit": ((1 - (mark_price / entry_price)) * leverage) * 100,
            "mark_price": mark_price,
        }

    def _calculate_position_metrics(self, raw_position: Any, market_info: dict[str, Any]) -> tuple[float, float, float]:
        """
        Calculate key metrics for an open position, including entry price, leverage, and mark price.

        :param raw_position: Raw position data from the contract.
        :param market_info: Dictionary containing market information.
        :return: Tuple containing entry price, leverage, and mark price.
        """
        index_token_address = market_info["index_token_address"]
        entry_price = self._calculate_entry_price(raw_position, index_token_address)
        leverage = self._calculate_leverage(raw_position)
        mark_price = self._get_mark_price(index_token_address)

        return entry_price, leverage, mark_price

    def _calculate_entry_price(self, raw_position: Any, index_token_address: str) -> float:
        """
        Calculate the entry price for the position.

        :param raw_position: Raw position data from the contract.
        :param index_token_address: Address of the index token.
        :return: Entry price as a float.
        """
        return (raw_position[1][0] / raw_position[1][1]) / 10 ** (
            30 - self.chain_tokens[index_token_address]["decimals"]
        )

    def _calculate_leverage(self, raw_position: Any) -> float:
        """
        Calculate the leverage for the position.

        :param raw_position: Raw position data from the contract.
        :return: Leverage as a float.
        """
        collateral_token_decimals = self.chain_tokens[raw_position[0][2]]["decimals"]
        return (raw_position[1][0] / 10**30) / (raw_position[1][2] / 10**collateral_token_decimals)

    def _get_mark_price(self, index_token_address: str) -> float:
        """
        Get the current mark price for the position from the Oracle.

        :param index_token_address: Address of the index token.
        :return: Mark price as a float.
        """
        prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
        return float(
            np.median(
                [
                    float(prices[index_token_address]["maxPriceFull"]),
                    float(prices[index_token_address]["minPriceFull"]),
                ]
            )
            / 10 ** (30 - self.chain_tokens[index_token_address]["decimals"])
        )

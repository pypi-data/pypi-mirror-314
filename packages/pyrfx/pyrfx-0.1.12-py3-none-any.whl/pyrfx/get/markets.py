import logging
from logging import Logger
from typing import Any

from eth_typing import ChecksumAddress
from web3.contract import Contract

from pyrfx.config_manager import ConfigManager
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import get_available_tokens, get_reader_contract


class Markets:
    """
    A class that handles the retrieval and management of market data, including token addresses and metadata.
    """

    def __init__(self, config: ConfigManager, log_level: int = logging.INFO) -> None:
        """
        Initialize the Markets class with a configuration object and logger.

        :param config: ConfigManager object containing chain configuration.
        :param log_level: Logging level for the logger.
        """
        self.config: ConfigManager = config

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self._prices: dict[str, dict[str, int]] = {}
        self.data: dict[ChecksumAddress, dict[str, Any]] = self._process_markets()

    def get_index_token_address(self, market_address: ChecksumAddress) -> ChecksumAddress:
        """
        Retrieve the index token address for a given market key.

        :param market_address: The address representing the market.
        :return: The index token address as a ChecksumAddress.
        """
        return self.config.to_checksum_address(self.data[market_address]["index_token_address"])

    def get_long_token_address(self, market_address: ChecksumAddress) -> ChecksumAddress:
        """
        Retrieve the long token address for a given market key.

        :param market_address: The address representing the market.
        :return: The long token address as a ChecksumAddress.
        """
        return self.config.to_checksum_address(self.data[market_address]["long_token_address"])

    def get_short_token_address(self, market_address: ChecksumAddress) -> ChecksumAddress:
        """
        Retrieve the short token address for a given market key.

        :param market_address: The address representing the market.
        :return: The short token address as a ChecksumAddress.
        """
        return self.config.to_checksum_address(self.data[market_address]["short_token_address"])

    def get_market_symbol(self, market_address: ChecksumAddress) -> str:
        """
        Retrieve the market symbol for a given market key.

        :param market_address: The address representing the market.
        :return: The market symbol as a string.
        """
        return self.data[market_address]["market_symbol"]

    def get_decimal_factor(self, market_address: ChecksumAddress, long: bool = False, short: bool = False) -> int:
        """
        Retrieve the decimal factor for a market, either for long or short tokens.

        :param market_address: The address representing the market.
        :param long: Flag to retrieve long token's decimal factor.
        :param short: Flag to retrieve short token's decimal factor.
        :return: The decimal factor as an integer.
        """
        if long:
            return self.data[market_address]["long_token_metadata"]["decimals"]
        elif short:
            return self.data[market_address]["short_token_metadata"]["decimals"]
        return self.data[market_address]["market_metadata"]["decimals"]

    def is_synthetic(self, market_address: ChecksumAddress) -> bool:
        """
        Check if a market is synthetic.

        :param market_address: The address representing the market.
        :return: True if the market is synthetic, otherwise False.
        """
        return self.data[market_address]["market_metadata"].get("synthetic", False)

    def is_swap_only(self, market_address: ChecksumAddress) -> bool:
        """
        Check if a market is swap only.

        :param market_address: The address representing the market.
        :return: True if the market is swap only, otherwise False.
        """
        return self.data[market_address]["is_swap_only"]

    def get_available_markets(self) -> dict[ChecksumAddress, dict[str, Any]]:
        """
        Get a dictionary of available markets for a given chain.

        :return: A dictionary containing the available markets.
        """
        return self.data

    def _get_available_markets_raw(self) -> list[tuple]:
        """
        Fetch the raw market data from the reader contract and transform each address into its checksum address.

        :return: A list of tuples containing the raw market data with checksum addresses.
        """
        reader_contract: Contract = get_reader_contract(self.config)
        raw_markets: list[tuple] = reader_contract.functions.getMarkets(
            self.config.contracts.data_store.contract_address, 0, 2**256 - 1
        ).call()

        # Transform each address in each tuple to a checksum address
        checksum_markets: list[tuple] = [
            tuple(self.config.to_checksum_address(address) for address in raw_market) for raw_market in raw_markets
        ]

        return checksum_markets

    def _process_markets(self) -> dict[ChecksumAddress, dict[str, Any]]:
        """
        Process the raw market data and structure it into a dictionary.

        :return: A dictionary containing the decoded market data.
        """
        available_tokens: dict[ChecksumAddress, dict[str, ChecksumAddress | int | bool]] = get_available_tokens(
            self.config
        )
        raw_markets: list[tuple] = self._get_available_markets_raw()
        markets_data: dict[ChecksumAddress, dict[str, Any]] = {}

        for raw_market in raw_markets:
            if not self._is_index_token_in_signed_prices_api(index_token_address=raw_market[1]):
                continue

            # Check if the market is SWAP-ONLY
            is_swap_only: bool = True if raw_market[1] == self.config.zero_address else False

            # Decode market symbol
            decoded_market_symbol: str = self._decode_symbol(
                market_symbol=available_tokens[raw_market[1]]["symbol"],
                is_swap_only=is_swap_only,
            )

            logging.debug(f"{raw_market} - {decoded_market_symbol}")
            markets_data[self.config.to_checksum_address(raw_market[0])] = self._decode_market_data(
                available_tokens=available_tokens, raw_market=raw_market, market_symbol=decoded_market_symbol
            )
            self.logger.info(
                f"Market processed: {markets_data[raw_market[0]]['rfx_market_address']} | "
                f"{markets_data[raw_market[0]]['market_symbol']:7}"
            )

        return markets_data

    @staticmethod
    def _decode_symbol(market_symbol: str, is_swap_only: bool) -> str:
        """
        Decode the market symbol into its full name.

        :param market_symbol: A string encoding the market details.
        :return: A decoded full market name.
        """
        if is_swap_only:
            return "SWAP-ONLY"

        if "/" not in market_symbol:
            suffix = "/USD"
        else:
            suffix = ""

        market_symbol: str = "BTC" if market_symbol == "WBTC" else market_symbol
        market_symbol: str = "ETH" if market_symbol == "WETH" else market_symbol

        return f"{market_symbol}{suffix}"

    @staticmethod
    def _decode_market_data(
        available_tokens: dict[str, dict[str, str | int | bool]],
        raw_market: tuple,
        market_symbol: str,
    ) -> dict[str, Any]:
        """
        Decode the raw market data into a structured dictionary.

        :param available_tokens: A dictionary mapping token addresses to metadata.
        :param raw_market: A tuple containing raw market data from the contract.
        :param market_symbol: The market symbol for the current market.
        :return: A dictionary containing the decoded market data.
        """
        if market_symbol == "SWAP-ONLY":
            market_metadata: dict[str, Any] = {
                "symbol": (
                    f"{market_symbol} "
                    f"[{available_tokens[raw_market[2]]['symbol']}-{available_tokens[raw_market[3]]['symbol']}]"
                )
            }
        else:
            market_metadata: dict[str, Any] = available_tokens.get(raw_market[1], {})

        market_symbol: str = (
            f"{market_symbol} [{available_tokens[raw_market[2]]['symbol']}-{available_tokens[raw_market[3]]['symbol']}]"
        )

        return {
            "rfx_market_address": raw_market[0],
            "market_symbol": market_symbol,
            "index_token_address": raw_market[1],
            "market_metadata": market_metadata,
            "long_token_metadata": available_tokens.get(raw_market[2], {}),
            "long_token_address": raw_market[2],
            "short_token_metadata": available_tokens.get(raw_market[3], {}),
            "short_token_address": raw_market[3],
            "is_swap_only": True if market_symbol == "SWAP-ONLY" else False,
        }

    def _is_index_token_in_signed_prices_api(self, index_token_address: str) -> bool:
        """
        Check if the index token is included in the signed prices API.

        :param index_token_address: The address of the index token.
        :return: True if the index token is present in the API, otherwise False.
        """
        try:
            if not self._prices:
                self._prices: dict[str, dict[str, int]] = OraclePrices(config=self.config).get_recent_prices()

            if index_token_address == self.config.zero_address:
                return True
            return bool(self._prices.get(index_token_address))

        except KeyError:
            self.logger.warning(f"Market {index_token_address} is not live on RFX.")
            return False

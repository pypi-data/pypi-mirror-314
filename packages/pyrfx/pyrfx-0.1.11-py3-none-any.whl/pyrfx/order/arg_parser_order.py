import logging
from typing import Any, Callable, Final

import numpy as np
from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.get.pool_tvl import PoolTVL
from pyrfx.order.swap_router import SwapRouter
from pyrfx.utils import get_available_tokens


class OrderArgumentParser:
    """
    A parser to handle and process order arguments for increase, decrease, or swap operations on the RFX Exchange.

    This class processes user-supplied order parameters, ensures all required parameters are present,
    fills in missing parameters where possible, and raises exceptions for critical missing data.

    :param config: Configuration object containing network details.
    :param operation_type: The type of operation ('increase', 'decrease', or 'swap').
    """

    def __init__(self, config: ConfigManager, operation_type: str) -> None:
        """
        Initializes the LiquidityArgumentParser class with the necessary configuration and operation type.

        :param config: Configuration object containing chain and market settings.
        :param operation_type: Specifies the type of operation ('increase', 'decrease', or 'swap').
        :raises ValueError: If an unknown operation type is provided.
        :return: None
        """
        self.config: ConfigManager = config
        self.parameters: dict = {}
        self.operation_type: str = operation_type
        self._allowed_operation_types: Final[list[str]] = ["increase", "decrease", "swap"]
        if operation_type not in self._allowed_operation_types:
            error_message: str = (
                f'Operation type {operation_type} is not valid. Valid types: {", ".join(self._allowed_operation_types)}'
            )
            logging.error(error_message)
            raise ValueError(error_message)

        # Set required keys based on operation type
        self.required_keys: list[str] = self._set_required_keys()

        self._available_markets: dict[str, dict[str, Any]] | None = None

        self.missing_base_key_methods: dict[str, Callable[[], None]] = {
            "collateral_address": self._handle_missing_collateral_address,
            "index_token_address": self._handle_missing_index_token_address,
            "initial_collateral_delta": self._handle_missing_initial_collateral_delta,
            "position_type": self._handle_missing_position_type,
            "leverage": self._handle_missing_leverage,
            "market_address": self._handle_missing_market_address,
            "out_token_address": self._handle_missing_out_token_address,
            "slippage_percent": self._handle_missing_slippage_percent,
            "start_token_address": self._handle_missing_start_token_address,
            "swap_path": self._handle_missing_swap_path,
        }

    def process_parameters(self, parameters: dict) -> dict[str, Any]:
        """
        Processes the input dictionary and fills in missing keys if possible. Raises exceptions if
        critical data is missing.

        The method:
        - Identifies missing keys in the supplied parameters.
        - Fills in missing data like `swap_path`, `collateral_address`, etc.
        - Validates parameters, including position size and maximum leverage limits for non-swap operations.

        :param parameters: Dictionary containing order parameters.
        :return: Processed dictionary with missing keys filled in.
        """
        self.parameters: dict[str, Any] = parameters
        missing_keys: list[str] = self._determine_missing_keys()

        for missing_key in missing_keys:
            if missing_key in self.missing_base_key_methods:
                self.missing_base_key_methods[missing_key]()

        if self.operation_type == "swap":
            self.calculate_missing_position_size_info_keys()
            self._check_if_max_leverage_exceeded()

        if self.operation_type == "increase" and self._calculate_initial_collateral_usd() < 2:
            raise Exception("Position size must be backed by >= $2 of collateral!")

        self._format_size_info()
        return self.parameters

    def _set_required_keys(self) -> list[str]:
        """
        Set the list of required keys based on the operation type (increase, decrease, or swap).

        :return: A list of required keys for the specified operation.
        """
        if self.operation_type == "increase":
            return [
                "index_token_address",
                "market_address",
                "start_token_address",
                "collateral_address",
                "swap_path",
                "position_type",
                "size_delta_usd",
                "initial_collateral_delta",
                "slippage_percent",
                "leverage",
            ]
        elif self.operation_type == "decrease":
            return [
                "index_token_address",
                "market_address",
                "start_token_address",
                "collateral_address",
                "position_type",
                "size_delta_usd",
                "initial_collateral_delta",
                "slippage_percent",
                "leverage",
            ]
        elif self.operation_type == "swap":
            return [
                "start_token_address",
                "out_token_address",
                "initial_collateral_delta",
                "swap_path",
                "slippage_percent",
                "leverage",
            ]
        else:
            return []

    def _determine_missing_keys(self) -> list:
        """
        Compare the supplied dictionary keys with the required keys for creating an order.

        :return: A list of missing keys.
        """
        return [key for key in self.required_keys if key not in self.parameters]

    def _handle_missing_index_token_address(self) -> None:
        """
        Handles missing 'index_token_address'. Attempts to infer the address from the token symbol.
        Raises an exception if neither index token address nor symbol is provided.

        :raises Exception: If neither index token address nor symbol is provided.
        :return: None.
        """
        token_symbol: str | None = self.parameters.get("market_symbol")

        if not token_symbol:
            logging.error("'market_symbol' does not exist in parameters!")
            raise Exception("'market_symbol' does not exist in parameters!")

        # TODO: possibly handle synthetic tokens that does not exist on zkSync

        # Retrieve the token address by symbol
        self.parameters["index_token_address"] = self._find_token_address_by_token_symbol(
            input_dict=get_available_tokens(config=self.config), token_symbol=token_symbol
        )

    def _handle_missing_market_address(self) -> None:
        """
        Handles the case where the 'market_address' is missing. Attempts to infer the market address based on the
        provided 'index_token_address'. Handles specific known exceptions for certain token addresses.
        Raises a ValueError if the 'index_token_address' is missing or if no market address can be inferred.

        :raises ValueError: If the 'index_token_address' is missing or cannot infer the market key.
        """
        if not self.parameters.get("market_symbol"):
            logging.error("Market symbol is missing.")
            raise ValueError("Market symbol is missing.")

        if not self.parameters.get("underlying_token_symbols"):
            logging.error("Underlying token symbols are missing.")
            raise ValueError("Underlying token symbols are missing.")

        # Attempt to find the market key from available markets using the index token address
        self.parameters["market_address"] = self._find_market_address(
            market_symbol=self.parameters["market_symbol"],
            underlying_token_symbols=self.parameters["underlying_token_symbols"],
        )

    def _find_market_address(self, market_symbol: str, underlying_token_symbols: dict[str, str]) -> str:
        """
        Finds the market address for the given index token address.

        :param market_symbol: Market symbol.
        :param underlying_token_symbols: The symbols of the underlying tokens.
        :return: The market key corresponding to the index token address.
        :raises ValueError: If the index token address is not found.
        """
        if not self._available_markets:
            self._available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(
                self.config
            ).get_available_markets()

        market_address: ChecksumAddress | None = None
        for rfx_market_address, market_info in self._available_markets.items():
            if (
                market_info["market_symbol"] == market_symbol
                and market_info["long_token_metadata"]["symbol"] == underlying_token_symbols["base_token_symbol"]
                and market_info["short_token_metadata"]["symbol"] == underlying_token_symbols["quote_token_symbol"]
            ):
                market_address: ChecksumAddress = rfx_market_address

        if market_address:
            logging.info(
                f"Market address found: {market_address} for market symbol: {market_symbol} and "
                f"underlying token symbols: {underlying_token_symbols}"
            )
            return market_address

        e_msg: str = (
            f"Market address was not found for market symbol: {market_symbol} and "
            f"underlying token symbols: {underlying_token_symbols}"
        )
        logging.error(e_msg)
        raise ValueError(e_msg)

    def _handle_missing_token_address(self, token_type: str, token_symbol_key: str, address_key: str) -> None:
        """
        General handler for missing token addresses. Infers the address from the token symbol.

        :param token_type: A string describing the type of token (e.g., 'start', 'out', 'collateral').
        :param token_symbol_key: The token symbol key in the parameters.
        :param address_key: The key to be retrieved and stored in the parameters.
        :raises ValueError: If the token symbol or address is not provided or cannot be inferred.
        """
        token_symbol: str | None = self.parameters.get(token_symbol_key)
        if not token_symbol:
            logging.error(f"{token_type.capitalize()} Token Address and Symbol not provided!")
            raise ValueError(f"{token_type.capitalize()} Token Address and Symbol not provided!")

        # Infer the token address from the symbol
        self.parameters[address_key] = self._find_token_address_by_token_symbol(
            input_dict=get_available_tokens(config=self.config), token_symbol=token_symbol
        )

    def _handle_missing_start_token_address(self) -> None:
        """
        Handles missing 'start_token_address'. Infers the address from the token symbol.
        """
        self._handle_missing_token_address(
            token_type="start", token_symbol_key="start_token_symbol", address_key="start_token_address"
        )

    def _handle_missing_out_token_address(self) -> None:
        """
        Handles missing 'out_token_address'. Infers the address from the token symbol.
        """
        self._handle_missing_token_address(
            token_type="out", token_symbol_key="out_token_symbol", address_key="out_token_address"
        )

    def _handle_missing_collateral_address(self) -> None:
        """
        Handles missing 'collateral_address'. Infers the address from the collateral token symbol.

        Validates whether the collateral can be used in the requested market.
        """
        self._handle_missing_token_address(
            token_type="collateral", token_symbol_key="collateral_token_symbol", address_key="collateral_address"
        )

        # Validate collateral usage
        collateral_address = self.parameters["collateral_address"]
        if self._check_if_valid_collateral_for_market(collateral_address) and self.operation_type != "swap":
            self.parameters["collateral_address"] = collateral_address

    @staticmethod
    def _find_token_address_by_token_symbol(
        input_dict: dict[ChecksumAddress, dict[str, ChecksumAddress | int | bool]], token_symbol: str
    ) -> ChecksumAddress:
        """
        Finds the token address in the input dictionary that matches the given token symbol.

        :param input_dict: Dictionary containing token information.
        :param token_symbol: The symbol of the token to search for.
        :return: The token address corresponding to the token symbol.
        :raises ValueError: If the token symbol is not found in the input dictionary.
        :return: None
        """
        address: ChecksumAddress | None = next(
            (k for k, v in input_dict.items() if v.get("symbol") == token_symbol), None
        )

        if address is None:
            logging.error(f'"{token_symbol}" is not a known token!')
            raise ValueError(f'"{token_symbol}" is not a known token!')

        return address

    def _handle_missing_swap_path(self) -> None:
        """
        Handles missing 'swap_path'. Determines the appropriate swap route based on the operation type
        and the relationship between the start, out, and collateral tokens.

        - If the operation is a token swap, the swap path is calculated between start and out tokens.
        - If the start token matches the collateral token, no swap path is needed.
        - Otherwise, the swap path is determined between the start token and collateral.

        :raises ValueError: If required tokens are missing and cannot determine the swap route.
        :return: None
        """
        start_address: ChecksumAddress | None = self.config.to_checksum_address(
            address=self.parameters.get("start_token_address")
        )
        if not start_address:
            logging.error("Start token address is missing!")
            raise ValueError("Start token address is missing!")

        if self.operation_type == "swap":
            out_address: ChecksumAddress | None = self.config.to_checksum_address(
                address=self.parameters.get("out_token_address")
            )
            if not out_address:
                raise ValueError("Out token address is missing!")

            self.parameters["swap_path"] = self._determine_swap_path(
                start_address=start_address, end_address=out_address
            )
        else:
            collateral_address: ChecksumAddress | None = self.config.to_checksum_address(
                self.parameters.get("collateral_address")
            )
            if not collateral_address:
                logging.error("Collateral address is missing!")
                raise ValueError("Collateral address is missing!")

            if start_address == collateral_address:
                self.parameters["swap_path"] = []
            else:
                self.parameters["swap_path"] = self._determine_swap_path(
                    start_address=start_address, end_address=collateral_address
                )

    def _determine_swap_path(self, start_address: ChecksumAddress, end_address: ChecksumAddress) -> list:
        """
        Determines the swap path between two token addresses using available markets.

        :param start_address: Address of the start token.
        :param end_address: Address of the end token.
        :return: The swap path as a list.
        """
        if not self._available_markets:
            self._available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(
                self.config
            ).get_available_markets()

        pool_tvl: dict[str, dict[str, Any]] = PoolTVL(config=self.config).get_pool_balances()
        swap_router: SwapRouter = SwapRouter(config=self.config, pool_tvl=pool_tvl)
        swap_route: list[ChecksumAddress] = swap_router.determine_swap_route(
            available_markets=self._available_markets,
            in_token_address=start_address,
            out_token_address=end_address,
        )
        return swap_route

    def _handle_missing_parameter(self, param_name: str, message: str) -> None:
        """
        General handler for missing parameters.

        :param param_name: The name of the missing parameter.
        :param message: The error message to display when the parameter is missing.
        :raises ValueError: Always raises a ValueError with the provided message.
        :return: None
        """
        raise ValueError(f"Missing parameter: {param_name}. {message}")

    def _handle_missing_position_type(self) -> None:
        """
        Handles the case where 'position_type' is missing from the parameter's dictionary.

        :raises ValueError: If 'position_type' is not provided, which indicates whether the position is long or short.
        :return: None
        """
        self._handle_missing_parameter(
            param_name="position_type",
            message=(
                "Please indicate if the position is "
                "long ('position_type': 'long') or "
                "short ('position_type': 'short')."
            ),
        )

    def _handle_missing_leverage(self) -> None:
        """
        Handles the case where 'leverage' is missing from the parameter's dictionary.

        :return: None
        """
        if self.operation_type == "swap" or self.operation_type == "decrease":
            self.parameters["leverage"] = 1
        elif self.operation_type == "increase":
            if not self.parameters.get("leverage"):
                logging.warning("Using default leverage 1!")
                self.parameters["leverage"] = 1
        else:
            logging.error("Leverage parameter is missing!")
            raise ValueError("Leverage parameter is missing!")

    def _handle_missing_slippage_percent(self) -> None:
        """
        Handles the case where 'slippage_percent' is missing from the parameter's dictionary.

        :raises ValueError: If 'slippage_percent' is not provided, which is the percentage of acceptable slippage.
        :return: None
        """
        self._handle_missing_parameter(
            param_name="slippage_percent", message="Please provide the slippage percentage ('slippage_percent')."
        )

    def _handle_missing_initial_collateral_delta(self) -> None:
        """
        Handles the case where 'initial_collateral_delta' is missing from the parameter's dictionary.

        :return:
        """
        if "size_delta_usd" in self.parameters and "leverage" in self.parameters:
            collateral_usd: float = self.parameters["size_delta_usd"] / self.parameters["leverage"]
            self.parameters["initial_collateral_delta"] = self._calculate_initial_collateral_tokens(collateral_usd)

    def _check_if_valid_collateral_for_market(self, collateral_address: str) -> bool:
        """
        Checks if the provided collateral address is valid for the requested market.

        :param collateral_address: The address of the collateral token.
        :return: True if valid collateral, otherwise raises a ValueError.
        """
        market_address: ChecksumAddress | None = self.parameters.get("market_address")

        # Fetch the market information
        if not self._available_markets:
            self._available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(
                self.config
            ).get_available_markets()
        market: dict | None = self._available_markets.get(market_address)

        if market and (
            collateral_address == market.get("long_token_address")
            or collateral_address == market.get("short_token_address")
        ):
            return True

        logging.error(f"Collateral {collateral_address} is not valid for the selected market.")
        raise ValueError(f"Collateral {collateral_address} is not valid for the selected market.")

    @staticmethod
    def find_key_by_symbol(input_dict: dict, search_symbol: str) -> str:
        """
        Finds the key (token address) in the input_dict that matches the provided symbol.

        :param input_dict: Dictionary of tokens with token symbols as values.
        :param search_symbol: The token symbol to search for.
        :return: The token address corresponding to the symbol.
        :raises ValueError: If the token symbol is not found.
        """
        key: str | None = next((key for key, value in input_dict.items() if value.get("symbol") == search_symbol), None)

        if key is None:
            logging.error(f'"{search_symbol}" not recognized as a valid token.')
            raise ValueError(f'"{search_symbol}" not recognized as a valid token.')

        return key

    def calculate_missing_position_size_info_keys(self) -> dict:
        """
        Calculates missing size-related parameters (e.g., size_delta_usd, initial_collateral_delta)
        if possible. Raises a ValueError if required parameters are missing.

        :raises ValueError: If the required parameters `size_delta_usd`, `initial_collateral_delta`, or `leverage`
            are missing, making the calculations impossible.
        :return: The updated parameters dictionary with `size_delta_usd` and `initial_collateral_delta` filled in, if
            calculated.
        """
        if "size_delta_usd" in self.parameters and "initial_collateral_delta" in self.parameters:
            return self.parameters

        if "leverage" in self.parameters and "initial_collateral_delta" in self.parameters:
            initial_collateral_usd: float = self._calculate_initial_collateral_usd()
            self.parameters["size_delta_usd"] = self.parameters["leverage"] * initial_collateral_usd
            return self.parameters

        if "size_delta_usd" in self.parameters and "leverage" in self.parameters:
            collateral_usd = self.parameters["size_delta_usd"] / self.parameters["leverage"]
            self.parameters["initial_collateral_delta"] = self._calculate_initial_collateral_tokens(collateral_usd)
            return self.parameters

        logging.error('Missing required keys: "size_delta_usd", "initial_collateral_delta", or "leverage".')
        raise ValueError('Missing required keys: "size_delta_usd", "initial_collateral_delta", or "leverage".')

    def _calculate_initial_collateral_usd(self) -> float:
        """
        Calculates the USD value of the collateral from the initial collateral delta.

        :return: The USD value of the initial collateral.
        """
        collateral_amount: float = self.parameters["initial_collateral_delta"]
        prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
        token_address: ChecksumAddress = self.parameters["start_token_address"]

        price: float = float(
            np.median([int(prices[token_address]["maxPriceFull"]), int(prices[token_address]["minPriceFull"])])
        )
        oracle_factor: int = get_available_tokens(config=self.config)[token_address]["decimals"] - 30

        return price * 10**oracle_factor * collateral_amount

    def _calculate_initial_collateral_tokens(self, collateral_usd: float) -> float:
        """
        Calculates the amount of tokens based on the collateral's USD value.

        :param collateral_usd: The dollar value of the collateral.
        :return: The amount of tokens equivalent to the collateral value.
        """
        prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
        token_address: ChecksumAddress = self.parameters["start_token_address"]

        price: float = float(
            np.median([int(prices[token_address]["maxPriceFull"]), int(prices[token_address]["minPriceFull"])])
        )
        oracle_factor: int = get_available_tokens(config=self.config)[token_address]["decimals"] - 30

        return collateral_usd / (price * 10**oracle_factor)

    def _format_size_info(self) -> None:
        """
        Formats size_delta and initial_collateral_delta to the correct precision for on-chain use.
        """
        if self.operation_type != "swap":
            self.parameters["size_delta"] = int(self.parameters["size_delta_usd"] * 10**30)

        decimal: int = get_available_tokens(config=self.config)[self.parameters["start_token_address"]]["decimals"]
        self.parameters["initial_collateral_delta"] = int(self.parameters["initial_collateral_delta"] * 10**decimal)

    def _check_if_max_leverage_exceeded(self):
        """
        Checks if the requested leverage exceeds the maximum allowed leverage.

        :raises ValueError: If the requested leverage exceeds the maximum limit.
        """
        collateral_usd_value: float = self._calculate_initial_collateral_usd()
        leverage_requested: float = self.parameters["size_delta_usd"] / collateral_usd_value

        # TODO: Example value, should be queried from the contract
        max_leverage: float = 100.0
        if leverage_requested > max_leverage:
            error_message: str = (
                f'Requested leverage "x{leverage_requested:.2f}" '
                f"exceeds the maximum allowed leverage of x{max_leverage}."
            )
            logging.error(error_message)
            raise ValueError(error_message)

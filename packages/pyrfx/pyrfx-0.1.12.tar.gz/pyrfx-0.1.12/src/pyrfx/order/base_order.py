import logging
from abc import ABC, abstractmethod
from logging import Logger

import numpy as np
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import BlockData, ChecksumAddress, TxParams

from pyrfx.config_manager import ConfigManager
from pyrfx.utils import PRECISION, get_exchange_router_contract


class Order(ABC):
    """
    A class to handle the creation, approval, and submission of orders.
    Handles different types of orders such as buy, sell, and swap with configurable gas fees, slippage, and collateral.
    """

    @abstractmethod
    def __init__(
        self,
        config: ConfigManager,
        market_address: ChecksumAddress,
        collateral_address: ChecksumAddress,
        index_token_address: ChecksumAddress,
        is_long: bool,
        size_delta: int,
        initial_collateral_delta: int,
        slippage_percent: float,
        order_type: str,
        swap_path: list | None,
        max_fee_per_gas: int | None = None,
        auto_cancel: bool = False,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initializes the Order class with the provided parameters and handles default behavior.

        :param config: Configuration manager containing blockchain settings.
        :param market_address: The address representing the RFX market.
        :param collateral_address: The contract address of the collateral token.
        :param index_token_address: The contract address of the index token.
        :param is_long: Boolean indicating whether the order is long or short.
        :param size_delta: Change in position size for the order.
        :param initial_collateral_delta: The amount of initial collateral in the order.
        :param slippage_percent: Allowed slippage for the price in percentage.
        :param order_type: The type of order to create.
        :param swap_path: List of contract addresses representing the swap path for token exchanges.
        :param max_fee_per_gas: Optional maximum gas fee to pay per gas unit. If not provided, calculated dynamically.
        :param auto_cancel: Boolean indicating whether the order should be auto-canceled if unfilled.
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        self.config: ConfigManager = config
        self.market_address: ChecksumAddress = market_address
        self.collateral_address: ChecksumAddress = collateral_address
        self.index_token_address: ChecksumAddress = index_token_address
        self.is_long: bool = is_long
        self.size_delta: int = size_delta
        self.initial_collateral_delta: int = initial_collateral_delta
        self.slippage_percent: float = slippage_percent
        self.order_type: str = order_type
        self.swap_path: list = swap_path if swap_path else []
        self.max_fee_per_gas: int | None = max_fee_per_gas
        self.auto_cancel: bool = auto_cancel
        self.debug_mode: bool = debug_mode

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self._gas_limits: dict = {}
        self._gas_limits_order_type_contract_function: ContractFunction | None = None

        # Dynamically calculate max_fee_per_gas if not provided
        if self.max_fee_per_gas is None:
            block: BlockData = self.config.connection.eth.get_block("latest")
            self.max_fee_per_gas: int = int(block["baseFeePerGas"] * 1.35)

        self._exchange_router_contract: Contract = get_exchange_router_contract(config=self.config)

    @abstractmethod
    def determine_gas_limits(self) -> None:
        """
        Determine and set gas limits for the order.
        This method is meant to be overridden by subclasses if custom gas limits are required.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def create_and_execute(self) -> None:
        """
        Build and submit an order, determining whether it is an open, close, or swap order, and ensuring correct gas
        limits, fees, and execution parameters are set.

        :raises Exception: If the execution price falls outside the acceptable range for the order type.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def _submit_transaction(self, value_amount: float, multicall_args: list) -> None:
        """
        Builds and submits the transaction to the network.

        :param value_amount: The amount of value (in native tokens) to send along with the transaction.
        :param multicall_args: List of arguments for multicall operations in the transaction.
        """
        self.logger.info("Building transaction ...")

        nonce: int = self.config.connection.eth.get_transaction_count(self.config.user_wallet_address)

        raw_txn: TxParams = self._exchange_router_contract.functions.multicall(multicall_args).build_transaction(
            {
                "value": value_amount,
                "chainId": self.config.chain_id,
                "gas": (2 * self._gas_limits_order_type_contract_function.call()),
                "maxFeePerGas": int(self.max_fee_per_gas),
                "maxPriorityFeePerGas": 0,
                "nonce": nonce,
            }
        )

        if not self.debug_mode:
            signed_txn: SignedTransaction = self.config.connection.eth.account.sign_transaction(
                raw_txn, self.config.private_key
            )
            tx_hash: HexBytes = self.config.connection.eth.send_raw_transaction(signed_txn.raw_transaction)

            tx_url: str = f"{self.config.block_explorer_url}/tx/0x{tx_hash.hex()}"
            self.logger.info(f"Transaction submitted! Transaction hash: 0x{tx_hash.hex()}")
            self.logger.info(f"Transaction submitted! Check status: {tx_url}")

    def _get_prices(self, decimals: float, prices: dict) -> tuple[float, int, float]:
        """
        Retrieves and calculates the acceptable prices for the order based on current market conditions and slippage.

        :param decimals: Decimal precision for the token.
        :param prices: Dictionary containing min and max prices from the Oracle.
        :return: A tuple containing the median price, slippage-adjusted price, and acceptable price in USD.
        """
        self.logger.info("Fetching current prices ...")

        price: float = float(
            np.median(
                [
                    float(prices[self.index_token_address]["maxPriceFull"]),
                    float(prices[self.index_token_address]["minPriceFull"]),
                ]
            )
        )

        if self.order_type == "increase":
            acceptable_price = int(price * (1 + self.slippage_percent if self.is_long else 1 - self.slippage_percent))
        elif self.order_type == "decrease":
            acceptable_price = int(price * (1 - self.slippage_percent if self.is_long else 1 + self.slippage_percent))
        else:
            acceptable_price = int(price)

        acceptable_price_in_usd: float = acceptable_price * 10 ** (decimals - PRECISION)

        self.logger.info(f"Mark Price: ${price * 10 ** (decimals - PRECISION):.6f}")
        self.logger.info(f"Acceptable price: ${acceptable_price_in_usd:.6f}")

        return price, acceptable_price, acceptable_price_in_usd

    def _create_order(self, arguments: tuple) -> HexBytes:
        """
        Create an order by encoding the contract function call.

        :param arguments: A tuple containing the necessary parameters for creating the order, such as wallet addresses,
                          market details, collateral amounts, and execution fees.
        :return: The ABI-encoded string representing the 'createOrder' contract function call.
        """
        return HexBytes(
            self._exchange_router_contract.encode_abi(
                "createOrder",
                args=[arguments],
            )
        )

    def _send_tokens(self, token_address: str, amount: int) -> HexBytes:
        """
        Send tokens to the exchange contract.

        :param token_address: The address of the token to send.
        :param amount: The amount of tokens to send.
        :return: The ABI-encoded string representing the 'sendTokens' contract function call.
        """
        return HexBytes(
            self._exchange_router_contract.encode_abi(
                "sendTokens",
                args=[token_address, self.config.contracts.order_vault.contract_address, amount],
            )
        )

    def _send_wnt(self, amount: int) -> HexBytes:
        """
        Send Wrapped Native Token (WNT) to the exchange contract.

        :param amount: The amount of WNT to send.
        :return: The ABI-encoded string representing the 'sendWnt' contract function call.
        """
        return HexBytes(
            self._exchange_router_contract.encode_abi(
                "sendWnt",
                args=[self.config.contracts.order_vault.contract_address, amount],
            )
        )

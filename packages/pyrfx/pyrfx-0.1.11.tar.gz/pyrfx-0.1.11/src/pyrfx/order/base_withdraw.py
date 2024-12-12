import logging
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any

from eth_account.datastructures import SignedTransaction
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import TxParams

from pyrfx.approve_token import check_if_approved
from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_execution_fee
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.get.pool_tvl import PoolTVL
from pyrfx.order.swap_router import SwapRouter
from pyrfx.utils import get_estimated_withdrawal_amount_out, get_exchange_router_contract


class Withdraw(ABC):
    @abstractmethod
    def __init__(
        self,
        config: ConfigManager,
        market_address: ChecksumAddress,
        out_token_address: ChecksumAddress,
        rp_amount: int,
        max_fee_per_gas: int | None = None,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initializes the Withdraw class, setting the configuration, market, token, and amount
        details. Establishes a connection and retrieves market information.

        :param config: Configuration object with chain and wallet details.
        :param market_address: The address representing the selected market.
        :param out_token_address: The token address for the withdrawal.
        :param rp_amount: The amount of RP tokens to withdraw.
        :param max_fee_per_gas: Optional; The maximum gas fee per transaction.
        :param debug_mode: Optional; Whether to run in debug mode.
        :param log_level: Logging level for this class.
        """
        self.config: ConfigManager = config
        self.market_address: ChecksumAddress = market_address
        self.out_token_address: ChecksumAddress = out_token_address
        self.rp_amount: int = rp_amount
        self.max_fee_per_gas: int | None = max_fee_per_gas
        self.debug_mode: bool = debug_mode

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.long_token_swap_path: list[ChecksumAddress] = []
        self.short_token_swap_path: list[ChecksumAddress] = []

        self._gas_limits: dict = {}
        self._gas_limits_order_type_contract_function: ContractFunction | None = None

        # Determine gas fee if not provided
        if self.max_fee_per_gas is None:
            block = self.config.connection.eth.get_block("latest")
            self.max_fee_per_gas: int = int(block["baseFeePerGas"] * 1.35)

        self._exchange_router_contract: Contract = get_exchange_router_contract(config=config)
        self._available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(config=config).get_available_markets()

    @abstractmethod
    def determine_gas_limits(self):
        """
        Placeholder for determining gas limits based on the transaction.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def _submit_transaction(self, value_amount: float, multicall_args: list) -> None:
        """
        Submits the transaction to the network after building it with the provided arguments.

        :param value_amount: The total value of the transaction in tokens.
        :param multicall_args: A list of arguments required for the multicall function.
        :return: None.
        """
        self.logger.info("Building transaction ...")

        nonce: int = self.config.connection.eth.get_transaction_count(self.config.user_wallet_address)

        # Build raw transaction
        raw_txn: TxParams = self._exchange_router_contract.functions.multicall(multicall_args).build_transaction(
            {
                "value": value_amount,
                "chainId": self.config.chain_id,
                "gas": int(2 * self._gas_limits_order_type_contract_function.call()),
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

            self.logger.info(f"Raw transaction: {signed_txn.raw_transaction.hex()}")

            tx_url: str = f"{self.config.block_explorer_url}/tx/0x{tx_hash.hex()}"
            self.logger.info(f"Transaction submitted! Transaction hash: 0x{tx_hash.hex()}")
            self.logger.info(f"Transaction submitted! Check status: {tx_url}")

    def create_and_execute(self) -> None:
        """
        Creates a withdrawal order, estimates fees, and builds the required transaction parameters.
        """
        self.determine_gas_limits()

        if not self.debug_mode:
            check_if_approved(
                config=self.config,
                spender_address=self.config.contracts.router.contract_address,
                token_to_approve_address=self.market_address,
                max_fee_per_gas=self.max_fee_per_gas,
                logger=self.logger,
            )

        # Estimate the minimum token amounts for withdrawal
        min_long_token_amount, min_short_token_amount = self._estimate_withdrawal()

        # Add a buffer to execution fees
        execution_fee: int = int(
            get_execution_fee(
                gas_limits=self._gas_limits,
                estimated_gas_limit_contract_function=self._gas_limits_order_type_contract_function,
                gas_price=self.config.connection.eth.gas_price,
            )
        )
        execution_fee: int = int(execution_fee * 3)

        # Determine swap paths for long and short tokens
        self._determine_swap_paths()

        # Build withdrawal arguments
        arguments: tuple = (
            self.config.user_wallet_address,
            self.config.zero_address,
            self.config.zero_address,
            self.market_address,
            self.long_token_swap_path,
            self.short_token_swap_path,
            min_long_token_amount,
            min_short_token_amount,
            True,  # Should unwrap native token
            execution_fee,
            0,  # Callback gas limit
        )

        multicall_args: list[HexBytes] = [
            # Send gas to withdraw vault
            self._send_wnt(execution_fee),
            # Send RP tokens to withdraw vault
            self._send_tokens(self.market_address, self.rp_amount),
            # Send swap parameters
            self._create_order(arguments),
        ]

        self.logger.info(f"Multicall arguments: {multicall_args}")

        # Submit the transaction with the built arguments
        self._submit_transaction(value_amount=execution_fee, multicall_args=multicall_args)

    def _determine_swap_paths(self) -> None:
        """
        Determine and calculate the swap paths for long and short tokens based on the current market.
        If the output token differs from the long or short token address, a swap route is calculated.

        This function checks both long and short token addresses and calculates swap paths
        using the `determine_swap_route` method. It gracefully handles any exceptions.
        """
        market: dict[str, Any] = self._available_markets[self.market_address]

        # Determine swap path for long token if different from output token
        if market["long_token_address"] != self.out_token_address:
            try:
                pool_tvl: dict[str, dict[str, Any]] = PoolTVL(config=self.config).get_pool_balances()
                swap_router: SwapRouter = SwapRouter(config=self.config, pool_tvl=pool_tvl)
                self.long_token_swap_path: list[ChecksumAddress] = swap_router.determine_swap_route(
                    available_markets=self._available_markets,
                    in_token_address=self.out_token_address,
                    out_token_address=market["long_token_address"],
                )
                self.logger.info(f"Long token swap path determined: {self.long_token_swap_path}")
            except Exception as e:
                self.logger.error(f"Failed to determine long token swap path: {str(e)}")

        # Determine swap path for short token if different from output token
        if market["short_token_address"] != self.out_token_address:
            try:
                pool_tvl: dict[str, dict[str, Any]] = PoolTVL(config=self.config).get_pool_balances()
                swap_router: SwapRouter = SwapRouter(config=self.config, pool_tvl=pool_tvl)
                self.short_token_swap_path: list[ChecksumAddress] = swap_router.determine_swap_route(
                    available_markets=self._available_markets,
                    in_token_address=self.out_token_address,
                    out_token_address=market["short_token_address"],
                )
                self.logger.info(f"Short token swap path determined: {self.short_token_swap_path}")
            except Exception as e:
                self.logger.error(f"Failed to determine short token swap path: {str(e)}")

    def _create_order(self, arguments: tuple) -> HexBytes:
        """
        Create a withdrawal order by encoding the ABI for the 'createWithdrawal' function.

        :param arguments: The arguments required for the createWithdrawal function.
        :return: Encoded ABI of the withdrawal order.
        """
        return HexBytes(
            self._exchange_router_contract.encode_abi(
                "createWithdrawal",
                args=[arguments],
            )
        )

    def _send_wnt(self, amount: int) -> HexBytes:
        """
        Send wrapped native tokens (WNT) to a predefined address.

        :param amount: The amount of WNT to send.
        :return: Encoded ABI for sending WNT.
        """
        return HexBytes(
            self._exchange_router_contract.encode_abi(
                "sendWnt",
                args=[self.config.contracts.withdrawal_vault.contract_address, amount],
            )
        )

    def _send_tokens(self, token_address, amount) -> HexBytes:
        """
        Send a specified amount of tokens to a predefined address.

        :param token_address: The address of the token to send.
        :param amount: The amount of tokens to send.
        :return: Encoded ABI for sending tokens.
        """
        return HexBytes(
            self._exchange_router_contract.encode_abi(
                "sendTokens",
                args=[token_address, self.config.contracts.withdrawal_vault.contract_address, amount],
            )
        )

    def _estimate_withdrawal(self):
        """
        Estimate the amount of long and short tokens to be output after burning RP tokens.

        This method queries the latest prices from the oracle, gathers relevant market information,
        and estimates the output amount of tokens (both long and short) based on the amount of RP tokens burned.

        :return: A list containing the estimated amounts of long and short tokens.
        """
        # Retrieve market and oracle price information
        market: dict[str, Any] = self._available_markets[self.market_address]
        oracle_prices_dict: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

        # Define relevant token addresses
        index_token_address: str = market["index_token_address"]
        long_token_address: str = market["long_token_address"]
        short_token_address: str = market["short_token_address"]

        # Assemble market addresses and price tuples
        market_addresses: list[str] = [
            self.market_address,
            index_token_address,
            long_token_address,
            short_token_address,
        ]
        prices: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] = (
            (
                int(oracle_prices_dict[index_token_address]["minPriceFull"]),
                int(oracle_prices_dict[index_token_address]["maxPriceFull"]),
            ),
            (
                int(oracle_prices_dict[long_token_address]["minPriceFull"]),
                int(oracle_prices_dict[long_token_address]["maxPriceFull"]),
            ),
            (
                int(oracle_prices_dict[short_token_address]["minPriceFull"]),
                int(oracle_prices_dict[short_token_address]["maxPriceFull"]),
            ),
        )

        # Define parameters for the withdrawal estimation
        parameters: dict[str, Any] = {
            "data_store_address": self.config.contracts.data_store.contract_address,
            "market_addresses": market_addresses,
            "token_prices_tuple": prices,
            "rp_amount": self.rp_amount,
            "ui_fee_receiver": self.config.zero_address,
        }

        # Return the estimated output amounts for long and short tokens
        return get_estimated_withdrawal_amount_out(self.config, parameters)

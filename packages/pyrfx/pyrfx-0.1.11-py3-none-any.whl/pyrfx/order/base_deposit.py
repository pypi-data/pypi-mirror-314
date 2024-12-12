import logging
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any

from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import BlockData, ChecksumAddress, TxParams

from pyrfx.approve_token import check_if_approved
from pyrfx.config_manager import ConfigManager
from pyrfx.custom_error_parser import CustomErrorParser
from pyrfx.gas_utils import get_execution_fee
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.get.pool_tvl import PoolTVL
from pyrfx.order.swap_router import SwapRouter
from pyrfx.utils import get_estimated_deposit_amount_out, get_exchange_router_contract


class Deposit(ABC):
    """
    A class to handle the creation and management of deposit orders in a decentralized exchange.

    This class is responsible for preparing deposit transactions, including setting up token paths,
    handling approvals, and submitting the final deposit transaction to the blockchain.
    It supports handling long and short token deposits, gas fee estimation, and token approvals.
    """

    @abstractmethod
    def __init__(
        self,
        config: ConfigManager,
        market_address: ChecksumAddress,
        initial_long_token_address: ChecksumAddress,
        initial_short_token_address: ChecksumAddress,
        long_token_amount: int,
        short_token_amount: int,
        max_fee_per_gas: int | None = None,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize the Deposit class with necessary configurations and contract objects.

        The constructor sets up various internal attributes based on the provided parameters, including
        initializing connections to blockchain contracts and retrieving market information. If `max_fee_per_gas`
        is not provided, it will be calculated based on the base fee of the latest block with a 35% multiplier.

        :param config: Configuration object containing blockchain network and contract settings.
        :param market_address: The address representing the market where the deposit will be made.
        :param initial_long_token_address: The address of the token to be deposited on the long side.
        :param initial_short_token_address: The address of the token to be deposited on the short side.
        :param long_token_amount: The amount of long tokens to be deposited in the market.
        :param short_token_amount: The amount of short tokens to be deposited in the market.
        :param max_fee_per_gas: Optional maximum gas fee to pay per gas unit. If not provided, calculated dynamically.
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        self.config: ConfigManager = config
        self.market_address: ChecksumAddress = market_address
        self.initial_long_token_address: ChecksumAddress = initial_long_token_address
        self.initial_short_token_address: ChecksumAddress = initial_short_token_address
        self.long_token_amount: int = long_token_amount
        self.short_token_amount: int = short_token_amount
        self.max_fee_per_gas: int = max_fee_per_gas or self._get_max_fee_per_gas()
        self.debug_mode: bool = debug_mode

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.long_token_swap_path: list = []
        self.short_token_swap_path: list = []

        self._gas_limits: dict = {}
        self._gas_limits_order_type_contract_function: ContractFunction | None = None

        # Internal setup of the blockchain connection and contracts
        self._exchange_router_contract: Contract = get_exchange_router_contract(config)
        self._available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(self.config).get_available_markets()

    @abstractmethod
    def determine_gas_limits(self) -> None:
        """
        Abstract method to determine gas limits for the deposit order.

        This method must be implemented by subclasses to handle the retrieval of
        gas limits specific to the operation being performed.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    def check_for_approval(self) -> None:
        """
        Check if the long and short tokens are approved for spending. If not, approve them.

        :raises ValueError: If token approval fails.
        """
        spender: ChecksumAddress = self.config.contracts.router.contract_address

        tokens_to_check: list[tuple[str, int]] = [
            (self.initial_long_token_address, self.long_token_amount),
            (self.initial_short_token_address, self.short_token_amount),
        ]

        tokens_to_approve: list[str] = [token for token, amount in tokens_to_check if amount > 0]

        if not tokens_to_approve:
            self.logger.info("No tokens need approval.")
            return

        for token_address in tokens_to_approve:
            try:
                check_if_approved(
                    config=self.config,
                    spender_address=spender,
                    token_to_approve_address=token_address,
                    max_fee_per_gas=self.max_fee_per_gas,
                    logger=self.logger,
                )
            except Exception as e:
                self.logger.error(f"Approval for token spending failed for {token_address}: {e}")
                raise ValueError(f"Approval for token spending failed for {token_address}: {e}")

    def create_and_execute(self) -> None:
        """
        Create a deposit order by estimating fees, setting up paths, and submitting the transaction.
        """
        try:
            # Check for token approvals unless in debug mode
            if not self.debug_mode:
                self.check_for_approval()

            min_market_tokens: int = self._estimate_deposit()
            execution_fee: int = int(
                get_execution_fee(
                    gas_limits=self._gas_limits,
                    estimated_gas_limit_contract_function=self._gas_limits_order_type_contract_function,
                    gas_price=self.config.connection.eth.gas_price,
                )
            )
            execution_fee: int = int(execution_fee * 3)

            # Validate initial tokens and determine swap paths
            self._check_initial_tokens()
            self._determine_swap_paths()

            arguments: tuple = (
                self.config.user_wallet_address,
                self.config.zero_address,
                self.config.zero_address,
                self.market_address,
                self.initial_long_token_address,
                self.initial_short_token_address,
                self.long_token_swap_path,
                self.short_token_swap_path,
                min_market_tokens,
                True,  # Should unwrap native token
                execution_fee,
                0,  # Callback gas limit
            )

            total_wnt_amount: int = 0
            multicall_args: list[HexBytes] = []

            if self.long_token_amount > 0:
                if self.initial_long_token_address == self.config.weth_address:
                    total_wnt_amount += self.long_token_amount
                else:
                    multicall_args.append(
                        self._send_tokens(
                            token_address=self.initial_long_token_address,
                            amount=self.long_token_amount,
                        )
                    )

            if self.short_token_amount > 0:
                if self.initial_short_token_address == self.config.weth_address:
                    total_wnt_amount += self.short_token_amount
                else:
                    multicall_args.append(
                        self._send_tokens(
                            token_address=self.initial_short_token_address,
                            amount=self.short_token_amount,
                        )
                    )

            # Send total WNT amount including deposit amount
            multicall_args.append(self._send_wnt(int(total_wnt_amount + execution_fee)))

            # Send our deposit parameters
            multicall_args.append(self._create_order(arguments))

            # Submit the final transaction
            self._submit_transaction(
                value_amount=int(total_wnt_amount + execution_fee),
                multicall_args=multicall_args,
            )

        except Exception as e:
            self.logger.error(f"Failed to create deposit order: {e}")
            # Try to parse error
            cap: CustomErrorParser = CustomErrorParser(config=self.config)
            error_reason: dict = cap.parse_error(error_bytes=e.args[0])
            error_message: str = cap.get_error_string(error_reason=error_reason)
            logging.info(f"Parsed error: {error_message}")

            raise

    def _get_max_fee_per_gas(self) -> int:
        """
        Retrieve the latest block base fee and calculate the max fee per gas with a multiplier.

        :return: Max fee per gas.
        """
        try:
            latest_block: BlockData = self.config.connection.eth.get_block("latest")
            base_fee_per_gas: int = latest_block.get("baseFeePerGas")

            if base_fee_per_gas is None:
                # Fallback mechanism or raise an error if EIP-1559 is not supported
                self.logger.error("Base fee per gas is not available for the latest block.")
                raise ValueError("Base fee per gas is not available for the latest block.")

            return int(base_fee_per_gas * 1.35)

        except Exception as e:
            self.logger.error(f"Failed to retrieve max fee per gas: {e}")
            raise

    def _submit_transaction(self, value_amount: float, multicall_args: list) -> None:
        """
        Submit the deposit transaction to the blockchain.

        :param value_amount: The amount of WNT (ETH or equivalent) to send with the transaction.
        :param multicall_args: A list of encoded contract function calls.
        :return: None.
        """
        self.logger.info("Building transaction ...")

        try:
            # Get the current nonce for the user’s wallet
            nonce: int = self.config.connection.eth.get_transaction_count(self.config.user_wallet_address)

            # Use the provided gas limits (or default to a safe estimate if not available)
            gas_estimate: int = self._gas_limits.get(
                "gas_estimate", 2 * self._gas_limits_order_type_contract_function.call()
            )
            max_fee_per_gas: int = self._gas_limits.get("max_fee_per_gas", int(self.max_fee_per_gas))
            max_priority_fee_per_gas: int = self._gas_limits.get("max_priority_fee_per_gas", 0)

            # Build the transaction using the provided gas limits
            raw_tx: TxParams = self._exchange_router_contract.functions.multicall(multicall_args).build_transaction(
                {
                    "value": value_amount,
                    "chainId": self.config.chain_id,
                    "gas": gas_estimate,
                    "maxFeePerGas": max_fee_per_gas,
                    "maxPriorityFeePerGas": max_priority_fee_per_gas,
                    "nonce": nonce,
                }
            )

            # Sign and submit the transaction if not in debug mode
            if not self.debug_mode:
                signed_txn: SignedTransaction = self.config.connection.eth.account.sign_transaction(
                    raw_tx, self.config.private_key
                )
                tx_hash: HexBytes = self.config.connection.eth.send_raw_transaction(signed_txn.raw_transaction)
                tx_url: str = f"{self.config.block_explorer_url}/tx/0x{tx_hash.hex()}"
                self.logger.info(f"Transaction submitted! Transaction hash: 0x{tx_hash.hex()}")
                self.logger.info(f"Transaction submitted! Check status: {tx_url}")

        except Exception as e:
            self.logger.error(f"Failed to submit transaction: {e}")
            raise Exception(f"Failed to submit transaction: {e}")

    def _check_initial_tokens(self) -> None:
        """
        Check and set long or short token addresses if they are not defined.

        :return: None.
        """
        for token_type, token_amount, token_key, token_name in [
            ("long", self.long_token_amount, "long_token_address", "initial_long_token"),
            ("short", self.short_token_amount, "short_token_address", "initial_short_token"),
        ]:
            if token_amount == 0:
                token_address: str = self._available_markets.get(self.market_address, {}).get(token_key)
                if not token_address:
                    raise ValueError(f"{token_type.capitalize()} token address is missing in the market info.")
                setattr(self, token_name, token_address)

    def _determine_swap_paths(self) -> None:
        """
        Determine the required swap paths for the long and short tokens if their current addresses differ from the
        market-defined ones.

        :return: None.
        """
        # Determine swap path for long token if needed
        swap_router: SwapRouter | None = None
        for token_type, initial_token, market_token_address, swap_path_attr in [
            ("long", self.initial_long_token_address, "long_token_address", "long_token_swap_path"),
            ("short", self.initial_short_token_address, "short_token_address", "short_token_swap_path"),
        ]:
            market_token_address: ChecksumAddress = self.config.to_checksum_address(
                self._available_markets[self.market_address][market_token_address]
            )
            if market_token_address != initial_token:
                if not swap_router:
                    pool_tvl: dict[str, dict[str, Any]] = PoolTVL(config=self.config).get_pool_balances()
                    swap_router: SwapRouter = SwapRouter(config=self.config, pool_tvl=pool_tvl)

                swap_path: list[ChecksumAddress] = swap_router.determine_swap_route(
                    available_markets=self._available_markets,
                    in_token_address=initial_token,
                    out_token_address=market_token_address,
                )

                setattr(self, swap_path_attr, swap_path)

    def _create_order(self, arguments: tuple) -> HexBytes:
        """
        Create the encoded order using the exchange contract's ABI.

        :param arguments: A tuple containing the arguments required for creating a deposit order.
        :return: Encoded transaction in HexBytes format.
        """
        if not arguments:
            logging.error("Transaction arguments must not be empty.")
            raise ValueError("Transaction arguments must not be empty.")
        return HexBytes(
            self._exchange_router_contract.encode_abi(
                "createDeposit",
                args=[arguments],
            )
        )

    def _send_tokens(self, token_address: str, amount: int) -> HexBytes:
        """
        Send tokens to the exchange contract.

        :param token_address: The token address to send.
        :param amount: The amount of tokens to send.
        :return: Encoded transaction in HexBytes format.
        """
        if not token_address or amount <= 0:
            logging.error("Invalid token address or amount")
            raise ValueError("Invalid token address or amount")
        return HexBytes(
            self._exchange_router_contract.encode_abi(
                "sendTokens",
                args=[token_address, self.config.contracts.deposit_vault.contract_address, amount],
            )
        )

    def _send_wnt(self, amount: int) -> HexBytes:
        """
        Send WNT to the exchange contract.

        :param amount: The amount of WNT to send.
        :return: Encoded transaction in HexBytes format.
        """
        if amount <= 0:
            logging.error("WNT amount must be greater than zero.")
            raise ValueError("WNT amount must be greater than zero.")
        return HexBytes(
            self._exchange_router_contract.encode_abi(
                "sendWnt",
                args=[self.config.contracts.deposit_vault.contract_address, amount],
            )
        )

    def _estimate_deposit(self) -> int:
        """
        Estimate the amount of RM tokens based on deposit amounts and current token prices.

        :return: Estimated RM tokens out.
        """
        oracle_prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

        # Extract market and token prices
        market_addresses, prices = self._get_market_data_and_prices(
            market=self._available_markets[self.market_address],
            oracle_prices=oracle_prices,
        )

        parameters: dict[str, Any] = {
            "data_store_address": self.config.contracts.data_store.contract_address,
            "market_addresses": market_addresses,
            "token_prices_tuple": prices,
            "long_token_amount": self.long_token_amount,
            "short_token_amount": self.short_token_amount,
            "ui_fee_receiver": self.config.zero_address,
        }

        return get_estimated_deposit_amount_out(config=self.config, params=parameters)

    def _get_market_data_and_prices(self, market: dict, oracle_prices: dict) -> tuple[list[str], list[tuple[int, int]]]:
        """
        Helper function to fetch market addresses and prices for the current market.

        :param market: Market information from all markets.
        :param oracle_prices: Dictionary of token prices fetched from Oracle.
        :return: A tuple containing market addresses and prices.
        """
        market_addresses = [
            self.market_address,
            market["index_token_address"],
            market["long_token_address"],
            market["short_token_address"],
        ]

        prices = [
            (int(oracle_prices[token]["minPriceFull"]), int(oracle_prices[token]["maxPriceFull"]))
            for token in [market["index_token_address"], market["long_token_address"], market["short_token_address"]]
        ]

        return market_addresses, prices

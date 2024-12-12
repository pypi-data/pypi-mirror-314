import logging
from logging import Logger
from typing import Any

from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3.contract import Contract
from web3.contract.contract import ContractFunction

from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_execution_fee, get_gas_limits
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.order.base_order import Order
from pyrfx.utils import (
    DecreasePositionSwapTypes,
    OrderTypes,
    get_data_store_contract,
    get_execution_price_and_price_impact,
)


class IncreaseOrder(Order):
    """
    A class to handle opening a buy order on the blockchain.
    Extends the base Order class to manage the logic for increasing (buy) orders.
    """

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
        swap_path: list | None = None,
        max_fee_per_gas: int | None = None,
        auto_cancel: bool = False,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize the IncreaseOrder class, extending the base Order class.

        :param config: Configuration manager containing blockchain settings.
        :param market_address: The address representing the RFX market.
        :param collateral_address: The contract address of the collateral token.
        :param index_token_address: The contract address of the index token.
        :param is_long: Boolean indicating whether the order is long or short.
        :param size_delta: Change in position size for the order.
        :param initial_collateral_delta: The amount of initial collateral in the order.
        :param slippage_percent: Allowed slippage for the price in percentage.
        :param swap_path: List of contract addresses representing the swap path for token exchanges.
        :param max_fee_per_gas: Optional maximum gas fee to pay per gas unit. If not provided, calculated dynamically.
        :param auto_cancel: Boolean indicating whether the order should be auto-canceled if unfilled.
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        # Call parent class constructor
        super().__init__(
            config=config,
            market_address=market_address,
            collateral_address=collateral_address,
            index_token_address=index_token_address,
            is_long=is_long,
            size_delta=size_delta,
            initial_collateral_delta=initial_collateral_delta,
            slippage_percent=slippage_percent,
            order_type="increase",
            swap_path=swap_path,
            max_fee_per_gas=max_fee_per_gas,
            auto_cancel=auto_cancel,
            debug_mode=debug_mode,
            log_level=log_level,
        )

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        # Determine gas limits
        self.determine_gas_limits()

    def determine_gas_limits(self) -> None:
        """
        Determine the gas limits required for placing an increase (buy) order.

        This method queries the datastore contract to get the relevant gas limits
        and sets the gas limit for the increase order operation.

        Logs an error if gas limits cannot be retrieved or if any other exception occurs.
        """
        try:
            # Retrieve the datastore contract
            datastore: Contract = get_data_store_contract(self.config)

            if not datastore:
                raise ValueError("Datastore contract was not found.")

            # Fetch the gas limits from the datastore
            self._gas_limits: dict[str, Any] = get_gas_limits(datastore)

            if not self._gas_limits:
                raise ValueError("Gas limits could not be retrieved.")

            # Retrieve the specific gas limit for the 'increase_order' operation
            self._gas_limits_order_type_contract_function: ContractFunction | None = self._gas_limits.get(
                "increase_order"
            )

            if not self._gas_limits_order_type_contract_function:
                raise KeyError("Gas limit for 'increase_order' not found.")

            if self.debug_mode:
                # Get the actual gas limit value by calling the contract function
                gas_limit_value: int = self._gas_limits_order_type_contract_function.call()
                self.logger.info(f"Gas limit for 'increase_order' is: {gas_limit_value}")

        except KeyError as e:
            self.logger.error(f"KeyError - Gas limit for 'increase_order' not found: {e}")
            raise Exception(f"Gas limit for 'increase_order' not found: {e}")

        except ValueError as e:
            self.logger.error(f"ValueError - Issue with datastore or gas limits: {e}")
            raise Exception(f"Error with datastore or gas limits: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error while determining gas limits: {e}")
            raise Exception(f"Unexpected error while determining gas limits: {e}")

    def create_and_execute(self) -> None:
        """
        Build and submit an increase order, ensuring correct gas limits, fees, and execution parameters are set.

        :raises Exception: If the execution price falls outside the acceptable range for the increase order.
        """
        # Set gas limits and execution fee
        self.determine_gas_limits()
        gas_price: int = self.config.connection.eth.gas_price
        execution_fee: int = int(
            get_execution_fee(
                gas_limits=self._gas_limits,
                estimated_gas_limit_contract_function=self._gas_limits_order_type_contract_function,
                gas_price=gas_price,
            )
        )
        execution_fee: int = int(execution_fee * 1.3)

        available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(config=self.config).get_available_markets()
        prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
        size_delta_price_price_impact: float = self.size_delta

        # Ensure wallet addresses are converted to checksum format
        collateral_address: ChecksumAddress = self.config.to_checksum_address(address=self.collateral_address)
        rfx_market_address: ChecksumAddress = self.config.to_checksum_address(address=self.market_address)

        # Parameters for calculating the execution price
        execution_price_parameters: dict[str, Any] = {
            "data_store_address": self.config.contracts.data_store.contract_address,
            "market_address": self.market_address,
            "index_token_price": [
                int(prices[self.index_token_address]["maxPriceFull"]),
                int(prices[self.index_token_address]["minPriceFull"]),
            ],
            "position_size_in_usd": 0,
            "position_size_in_tokens": 0,
            "size_delta": size_delta_price_price_impact,
            "is_long": self.is_long,
        }

        # Retrieve market details and calculate price based on slippage
        decimals: int = available_markets[self.market_address]["market_metadata"]["decimals"]
        price, acceptable_price, acceptable_price_in_usd = self._get_prices(decimals=decimals, prices=prices)

        # Set mark price for open positions
        mark_price: int = int(price)

        # Calculate execution price and its impact
        execution_price_and_price_impact: dict[str, float] = get_execution_price_and_price_impact(
            config=self.config, params=execution_price_parameters, decimals=decimals
        )
        self.logger.info(f"Execution price: ${execution_price_and_price_impact['execution_price']:.4f}")

        # Check if execution price is within acceptable range
        if (self.is_long and execution_price_and_price_impact["execution_price"] > acceptable_price_in_usd) or (
            not self.is_long and execution_price_and_price_impact["execution_price"] < acceptable_price_in_usd
        ):
            logging.error("Execution price falls outside the acceptable range! (order_type = 'increase')")
            raise Exception("Execution price falls outside the acceptable range! (order_type = 'increase')")

        # Build the order arguments
        arguments = (
            (
                self.config.user_wallet_address,
                self.config.user_wallet_address,  # Cancellation receiver
                self.config.zero_address,
                self.config.zero_address,
                rfx_market_address,
                collateral_address,
                self.swap_path,
            ),
            (
                self.size_delta,
                self.initial_collateral_delta,
                mark_price,
                acceptable_price,
                execution_fee,
                0,  # Callback gas limit
                0,  # Min output amount
            ),
            OrderTypes.MARKET_INCREASE.value,
            DecreasePositionSwapTypes.NO_SWAP.value,
            self.is_long,
            True,  # Should unwrap native token
            self.auto_cancel,
            HexBytes("0x" + "0" * 64),  # Referral code
        )

        if collateral_address == self.config.weth_address:
            value_amount = self.initial_collateral_delta + execution_fee
            multicall_args: list[HexBytes] = [self._send_wnt(value_amount), self._create_order(arguments)]
        else:
            value_amount = execution_fee
            multicall_args: list[HexBytes] = [
                self._send_wnt(value_amount),
                self._send_tokens(self.collateral_address, self.initial_collateral_delta),
                self._create_order(arguments),
            ]

        # Submit the transaction
        self._submit_transaction(value_amount=value_amount, multicall_args=multicall_args)

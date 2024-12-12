import logging
from logging import Logger

from eth_typing import ChecksumAddress
from web3.contract import Contract
from web3.contract.contract import ContractFunction

from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_gas_limits
from pyrfx.order.base_withdraw import Withdraw
from pyrfx.utils import get_data_store_contract


class WithdrawOrder(Withdraw):
    """
    A class to handle opening a withdrawal order.
    Extends the base Withdraw class to create and manage withdrawal orders.
    """

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
        Initialize the WithdrawOrder class, extending the base Withdraw class.

        :param config: Configuration object with chain and wallet details.
        :param market_address: The address representing the selected market.
        :param out_token_address: The token address for the withdrawal.
        :param rp_amount: The amount of RP tokens to withdraw.
        :param max_fee_per_gas: Maximum gas fee per transaction.
        :param debug_mode: Optional; Whether to run in debug mode.
        :param log_level: Logging level for this class.
        """
        # Call parent class constructor
        super().__init__(
            config=config,
            market_address=market_address,
            out_token_address=out_token_address,
            rp_amount=rp_amount,
            max_fee_per_gas=max_fee_per_gas,
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
        Determine the gas limits required for placing a withdrawal order.

        This method queries the datastore contract to fetch the relevant gas limits
        and sets the gas limit for the withdrawal operation. Provides a fallback if
        gas limits cannot be retrieved and logs any errors or issues encountered.
        """
        try:
            # Retrieve the datastore contract
            datastore: Contract = get_data_store_contract(self.config)

            if not datastore:
                raise ValueError("Datastore contract was not found.")

            # Fetch the gas limits from the datastore contract
            self._gas_limits: dict[str, ContractFunction] = get_gas_limits(datastore)

            if not self._gas_limits:
                raise ValueError("Gas limits could not be retrieved.")

            # Retrieve the specific gas limit for the 'withdraw_order' function
            self._gas_limits_order_type_contract_function: ContractFunction | None = self._gas_limits.get("withdraw")

            if not self._gas_limits_order_type_contract_function:
                raise ValueError("'withdraw_order' contract function was not found.")

            if self.debug_mode:
                # Get the actual gas limit value by calling the contract function
                gas_limit_value: int = self._gas_limits_order_type_contract_function.call()
                self.logger.info(f"Gas limit for 'withdraw_order' is: {gas_limit_value}")

        except KeyError as e:
            self.logger.error(f"KeyError - Gas limit for 'withdraw_order' not found: {e}")
            raise Exception(f"Gas limit for 'withdraw_order' not found: {e}")

        except ValueError as e:
            self.logger.error(f"ValueError - Issue with datastore or gas limits: {e}")
            raise Exception(f"Error with datastore or gas limits: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error while determining gas limits: {e}")
            raise Exception(f"Unexpected error while determining gas limits: {e}")

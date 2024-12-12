import logging
from logging import Logger

from eth_typing import ChecksumAddress
from web3.contract import Contract
from web3.contract.contract import ContractFunction

from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_gas_limits
from pyrfx.order.base_deposit import Deposit
from pyrfx.utils import get_data_store_contract


class DepositOrder(Deposit):
    """
    Class to handle the creation of a deposit order.
    Extends the base Deposit class to handle logic specific to deposit orders.
    """

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
        Initialize the DepositOrder class,extending the base Deposit class.

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
        super().__init__(
            config=config,
            market_address=market_address,
            initial_long_token_address=initial_long_token_address,
            initial_short_token_address=initial_short_token_address,
            long_token_amount=long_token_amount,
            short_token_amount=short_token_amount,
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
        Determine the gas limits for creating a deposit order by querying the datastore contract.

        This method retrieves the appropriate gas limits from the datastore and sets the gas limit
        for deposit order operations.

        Logs an error if gas limits cannot be retrieved or if any other exception occurs.
        """
        try:
            # Retrieve the datastore contract
            datastore: Contract = get_data_store_contract(self.config)

            if not datastore:
                self.logger.error("Datastore contract was not found.")
                raise ValueError("Datastore contract was not found.")

            # Fetch the gas limits from the datastore
            self._gas_limits: dict[str, ContractFunction] = get_gas_limits(datastore)

            if not self._gas_limits:
                self.logger.error("Gas limits could not be retrieved.")
                raise ValueError("Gas limits could not be retrieved.")

            # Retrieve the specific gas limit for the 'multiple_deposit' operation
            self._gas_limits_order_type_contract_function: ContractFunction | None = self._gas_limits.get(
                "multiple_deposit"
            )

            if not self._gas_limits_order_type_contract_function:
                self.logger.error("Gas limit for 'deposit' not found in the datastore response.")
                raise KeyError("Gas limit for 'deposit' not found in the datastore response.")

            if self.debug_mode:
                # Get the actual gas limit value by calling the contract function
                gas_limit_value: int = self._gas_limits_order_type_contract_function.call()
                self.logger.info(f"Gas limit for 'deposit' is: {gas_limit_value}")

        except KeyError as e:
            self.logger.error(f"KeyError - Gas limit for 'deposit' not found: {e}")
            raise Exception(f"Gas limit for 'deposit' not found: {e}")

        except ValueError as e:
            self.logger.error(f"ValueError - Issue with datastore or gas limits: {e}")
            raise Exception(f"Error with datastore or gas limits: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error while determining gas limits: {e}")
            raise Exception(f"Unexpected error while determining gas limits: {e}")

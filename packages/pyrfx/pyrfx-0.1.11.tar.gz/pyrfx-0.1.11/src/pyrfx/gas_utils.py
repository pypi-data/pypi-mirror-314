from web3.contract import Contract
from web3.contract.contract import ContractFunction

from pyrfx.keys import KEYS, deposit_gas_limit_key
from pyrfx.utils import apply_factor


def get_execution_fee(
    gas_limits: dict[str, ContractFunction], estimated_gas_limit_contract_function: ContractFunction, gas_price: int
) -> int:
    """
    Calculate the minimum execution fee required to perform an action based on gas limits and gas price.

    :param gas_limits: A dictionary of uncalled datastore limit functions.
    :param estimated_gas_limit_contract_function: The uncalled datastore contract function specific to the operation
        being undertaken.
    :param gas_price: The current gas price.
    :return: The adjusted gas fee to cover the execution cost.
    """
    base_gas_limit: int = gas_limits["execution_base_amount"].call()
    multiplier_factor: int = gas_limits["execution_multiplier_factor"].call()
    estimated_gas: int = estimated_gas_limit_contract_function.call()

    adjusted_gas_limit: int = base_gas_limit + apply_factor(estimated_gas, multiplier_factor)

    return int(adjusted_gas_limit * gas_price)


def get_gas_limits(datastore_object: Contract) -> dict[str, ContractFunction]:
    """
    Retrieve gas limit functions from the datastore contract for various operations requiring execution fees.

    :param datastore_object: A Web3 contract object for accessing the datastore.
    :return: A dictionary of uncalled gas limit functions corresponding to various operations.
    """
    gas_limits: dict[str, ContractFunction] = {
        "single_deposit": datastore_object.functions.getUint(deposit_gas_limit_key(single_token=True)),
        "multiple_deposit": datastore_object.functions.getUint(deposit_gas_limit_key(single_token=False)),
        "decrease_order": datastore_object.functions.getUint(KEYS["DECREASE_ORDER_GAS_LIMIT"]),
        "increase_order": datastore_object.functions.getUint(KEYS["INCREASE_ORDER_GAS_LIMIT"]),
        "single_swap_order": datastore_object.functions.getUint(KEYS["SINGLE_SWAP_GAS_LIMIT"]),
        "multiple_swap_order": datastore_object.functions.getUint(KEYS["SWAP_ORDER_GAS_LIMIT"]),
        "withdraw": datastore_object.functions.getUint(KEYS["WITHDRAWAL_GAS_LIMIT"]),
        "execution_base_amount": datastore_object.functions.getUint(KEYS["EXECUTION_GAS_FEE_BASE_AMOUNT"]),
        "execution_multiplier_factor": datastore_object.functions.getUint(KEYS["EXECUTION_GAS_FEE_MULTIPLIER_FACTOR"]),
    }

    return gas_limits

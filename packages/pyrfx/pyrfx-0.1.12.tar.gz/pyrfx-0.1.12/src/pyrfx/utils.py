import json
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Final

import pandas as pd
import requests
from eth_abi import encode
from eth_account import Account
from eth_typing import ChecksumAddress
from pandas import DataFrame
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt, wait_exponential
from web3 import Web3
from web3.contract import Contract

from pyrfx.config_manager import ConfigManager
from pyrfx.custom_error_parser import CustomErrorParser

PRECISION: Final[int] = 30


# Enum for Order Types
class OrderTypes(Enum):
    MARKET_SWAP = 0
    LIMIT_SWAP = 1
    MARKET_INCREASE = 2
    LIMIT_INCREASE = 3
    MARKET_DECREASE = 4
    LIMIT_DECREASE = 5
    STOP_LOSS_DECREASE = 6
    LIQUIDATION = 7


# Enum for Decrease Position Swap Types
class DecreasePositionSwapTypes(Enum):
    NO_SWAP = 0
    SWAP_PNL_TOKEN_TO_COLLATERAL_TOKEN = 1
    SWAP_COLLATERAL_TOKEN_TO_PNL_TOKEN = 2


# Enum for Swap
class SwapPricingTypes(Enum):
    TWO_STEPS = 0
    SHIFT = 1
    ATOMIC = 2


# Constants for rate limiting
CALLS_PER_SECOND: Final[int] = 3
ONE_SECOND: Final[int] = 1


# Combined retrier and rate limiter decorator
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
@sleep_and_retry
@limits(calls=CALLS_PER_SECOND, period=ONE_SECOND)
def execute_call(call) -> Any:
    """
    Executes a Web3 call with retry logic and rate limiting.

    :param call: Web3 call to be executed.
    :return: The result of the Web3 call.
    """
    result = call.call()
    logging.debug("Web3 call executed successfully.")
    return result


# Executes multiple Web3 calls concurrently using ThreadPoolExecutor
def execute_threading(function_calls: list) -> list:
    """
    Execute multiple Web3 function calls concurrently using ThreadPoolExecutor.

    :param function_calls: A list of Web3 function calls to execute.
    :return: A list of results from the executed Web3 calls.
    """
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(execute_call, function_calls))
    logging.info("All Web3 calls executed successfully.")
    return results


def load_contract_abi(abi_file_path: Path) -> list[dict[str, Any]]:
    """
    Load the ABI file from the specified path.

    :param abi_file_path: Path to the ABI JSON file.
    :return: Loaded ABI as a list of dictionaries.
    :raises FileNotFoundError: If the file doesn't exist.
    :raises json.JSONDecodeError: If the JSON content is invalid.
    """
    try:
        return json.loads(abi_file_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading ABI from {abi_file_path}: {e}")
        raise


def get_token_balance_contract(config: ConfigManager, contract_address: str) -> Contract | None:
    """
    Retrieve the contract object required to query a user's token balance.

    :param config: Configuration object containing RPC and chain details.
    :param contract_address: The token contract address to query balance from.
    :return: Web3 contract object or None if an error occurs.
    """
    abi_file_path = Path(__file__).parent / "contracts" / "balance_abi.json"

    try:
        # Load contract ABI and instantiate the contract
        contract_abi = load_contract_abi(abi_file_path)
        checksum_address = config.to_checksum_address(contract_address)
        contract = config.connection.eth.contract(address=checksum_address, abi=contract_abi)
        logging.debug(f"Contract for token balance at address {checksum_address} successfully created.")
        return contract
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading ABI or creating contract for address '{contract_address}': {e}")
        return None


def get_available_tokens(config: ConfigManager) -> dict[ChecksumAddress, dict[str, ChecksumAddress | int | bool]]:
    """
    Query the RFX API to generate a dictionary of available tokens for the specified chain.

    :param config: Configuration object containing the chain information.
    :return: Dictionary of available tokens.
    """
    try:
        response = requests.get(config.tokens_url)
        # Raise an HTTPError for bad responses
        response.raise_for_status()
        token_infos = response.json().get("tokens", [])
        logging.debug(f"Successfully fetched available tokens for chain {config.chain}.")

        # Ensure that address is in ChecksumAddress format
        processed_data: dict[ChecksumAddress, dict[str, ChecksumAddress | int | bool]] = {}
        for token_info in token_infos:
            token_info["address"] = config.to_checksum_address(token_info["address"])
            processed_data[token_info["address"]] = token_info

        return processed_data

    except requests.RequestException as e:
        logging.error(f"Error fetching tokens from API for chain {config.chain}: {e}")
        return {}


def get_contract(config: ConfigManager, contract_name: str) -> Contract:
    """
    Retrieve a contract object for the specified contract name and chain.

    :param config: Configuration object containing blockchain settings.
    :param contract_name: Name of the contract to retrieve.
    :return: Web3 contract object for the specified contract.
    :raises ValueError: If the contract information or ABI file is missing or invalid.
    :raises FileNotFoundError: If the ABI file is not found.
    :raises json.JSONDecodeError: If the ABI file is not valid JSON.
    """
    try:
        # Retrieve contract information
        contract_info = config.contracts[contract_name]

        # Load contract ABI
        abi_file_path = Path(__file__).parent / contract_info.abi_path
        logging.info(f"Loading ABI file from {abi_file_path}")
        contract_abi = load_contract_abi(abi_file_path)

        # Instantiate and return the Web3 contract object
        contract = config.connection.eth.contract(address=contract_info.contract_address, abi=contract_abi)
        logging.info(f"Contract object for '{contract_name}' on chain '{config.chain}' created successfully.")
        return contract

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading ABI for contract '{contract_name}': {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error while creating contract object '{contract_name}': {e}")
        raise


def get_reader_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the reader contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the reader.
    """
    return get_contract(config, "reader")


def get_event_emitter_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the event emitter contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the event emitter.
    """
    return get_contract(config, "event_emitter")


def get_data_store_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the data store contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the data store.
    """
    return get_contract(config, "data_store")


def get_exchange_router_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the exchange router contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the exchange router.
    """
    return get_contract(config, "exchange_router")


def create_signer(config: ConfigManager) -> Account | None:
    """
    Create a signer for the given chain using the private key.

    :param config: Configuration object containing the private key and chain information.
    :return: Web3 account object initialized with the private key.
    :raises ValueError: If the private key is missing or invalid.
    """
    if not config.private_key:
        raise ValueError("Private key is missing in the configuration.")

    return config.connection.eth.account.from_key(config.private_key)


def create_hash(data_types: list[str], data_values: list) -> bytes:
    """
    Create a keccak hash using a list of data types and their corresponding values.

    :param data_types: List of data types as strings.
    :param data_values: List of values corresponding to the data types.
    :return: Encoded and hashed key in bytes.
    """
    return Web3.keccak(encode(data_types, data_values))


def create_hash_string(string: str) -> bytes:
    """
    Create a keccak hash for a given string.

    :param string: The string to hash.
    :return: Hashed string in bytes.
    """
    return create_hash(["string"], [string])


def get_execution_price_and_price_impact(
    config: ConfigManager, params: dict[str, Any], decimals: int
) -> dict[str, float]:
    """
    Get the execution price and price impact for a position.

    :param config: Configuration object.
    :param params: Dictionary of the position parameters.
    :param decimals: Number of decimals for the token being traded.
    :return: A dictionary containing the execution price and price impact.
    """
    reader_contract = get_reader_contract(config)

    output = reader_contract.functions.getExecutionPrice(
        params.get("data_store_address"),
        params.get("market_address"),
        params.get("index_token_price"),
        params.get("position_size_in_usd"),
        params.get("position_size_in_tokens"),
        params.get("size_delta"),
        params.get("is_long"),
    ).call()

    return {
        "execution_price": (output[2] / pow(10, 30 - decimals)) if output else 0.0,
        "price_impact_usd": (output[0] / pow(10, 30)) if output else 0.0,
    }


def get_estimated_swap_output(config: ConfigManager, params: dict[str, Any]) -> dict[str, float]:
    """
    Get the estimated swap output amount and price impact for a given chain and swap parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the swap parameters.
    :return: A dictionary with the estimated token output and price impact.
    """
    try:
        reader_contract: Contract = get_reader_contract(config)
        output: tuple[int, int, tuple] = reader_contract.functions.getSwapAmountOut(
            params.get("data_store_address"),
            params.get("market_addresses"),
            params.get("token_prices_tuple"),
            params.get("token_in"),
            params.get("token_amount_in"),
            params.get("ui_fee_receiver"),
        ).call()
    except Exception as e:
        logging.error(f"Failed to get swap output: {e}")
        logging.info("Trying to decode custom error ...")

        cap: CustomErrorParser = CustomErrorParser(config=config)
        error_reason: dict = cap.parse_error(error_bytes=e.args[0])
        error_message: str = cap.get_error_string(error_reason=error_reason)
        logging.info(f"Parsed custom error: {error_message}")

        raise Exception("Failed to get swap output.")

    return {
        "out_token_amount": output[0],
        "price_impact_usd": output[1],
    }


def get_estimated_deposit_amount_out(config: ConfigManager, params: dict[str, Any]) -> int | None:
    """
    Get the estimated deposit amount output for a given chain and deposit parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the deposit parameters.
    :return: The output of the deposit amount calculation or None if an error occurs.
    """
    reader: Contract = get_reader_contract(config)

    output: int = reader.functions.getDepositAmountOut(
        params.get("data_store_address"),
        params.get("market_addresses"),
        params.get("token_prices_tuple"),
        params.get("long_token_amount"),
        params.get("short_token_amount"),
        params.get("ui_fee_receiver"),
        SwapPricingTypes.TWO_STEPS.value,
        True,
    ).call()

    return output


def get_estimated_withdrawal_amount_out(config: ConfigManager, params: dict[str, Any]) -> Any | None:
    """
    Get the estimated withdrawal amount output for a given chain and withdrawal parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the withdrawal parameters.
    :return: The output of the withdrawal amount calculation or None if an error occurs.
    """
    reader: Contract = get_reader_contract(config)

    output: int = reader.functions.getWithdrawalAmountOut(
        params.get("data_store_address"),
        params.get("market_addresses"),
        params.get("token_prices_tuple"),
        params.get("rp_amount"),
        params.get("ui_fee_receiver"),
        SwapPricingTypes.TWO_STEPS.value,
    ).call()

    return output


def find_dictionary_by_key_value(outer_dict: dict[str, dict], key: str, value: str) -> dict[str, Any] | None:
    """
    Search for a dictionary by key-value pair within an outer dictionary.

    :param outer_dict: The outer dictionary to search.
    :param key: The key to search for.
    :param value: The value to match.
    :return: The dictionary containing the matching key-value pair, or None if not found.
    """
    result: dict[str, Any] = next(
        (inner_dict for inner_dict in outer_dict.values() if inner_dict.get(key) == value), None
    )
    if result:
        logging.debug(f"Found dictionary for key={key}, value={value}")
    else:
        logging.error(f"No dictionary found for key={key}, value={value}")
        raise Exception(f"No dictionary found for key={key}, value={value}")
    return result


def save_json(output_data_path: Path, file_name: str, data: dict) -> None:
    """
    Save a dictionary as a JSON file in the specified directory.

    :param output_data_path: The output data path.
    :param file_name: Name of the JSON file.
    :param data: Dictionary data to save.
    """
    output_data_path.mkdir(parents=True, exist_ok=True)
    file_path = output_data_path / file_name

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logging.info(f"Data saved to: {file_path}")


def save_csv(output_data_path: Path, file_name: str, data: DataFrame) -> None:
    """
    Save a Pandas DataFrame as a CSV file in the specified directory.

    :param output_data_path: The output data path.
    :param file_name: Name of the CSV file.
    :param data: Pandas DataFrame to save.
    """
    output_data_path.mkdir(parents=True, exist_ok=True)
    file_path = output_data_path / file_name

    # Append to existing file if it exists
    if file_path.exists():
        existing_data = pd.read_csv(file_path)
        data = pd.concat([existing_data, data], ignore_index=True)

    data.to_csv(file_path, index=False)
    logging.info(f"Dataframe saved to: {file_path}")


def timestamp_df(data: dict) -> DataFrame:
    """
    Convert a dictionary into a Pandas DataFrame with a timestamp column.

    :param data: Dictionary data to convert.
    :return: DataFrame with timestamp column added.
    """
    data["timestamp"] = datetime.now(timezone.utc)
    return DataFrame([data])

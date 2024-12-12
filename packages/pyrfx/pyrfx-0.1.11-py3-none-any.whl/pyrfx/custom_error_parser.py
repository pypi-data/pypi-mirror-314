import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any, Final, Type

from eth_abi import decode
from eth_utils import decode_hex, keccak
from web3.contract import Contract

from pyrfx.config_manager import ConfigManager


class CustomErrorParser:
    """
    A class to parse custom Solidity errors using ABI and error bytes.
    """

    PANIC_MAP: Final[dict[int, str]] = {
        0x00: "Generic compiler inserted panics.",
        0x01: "Call assert with an argument that evaluates to false.",
        0x11: "Arithmetic operation results in underflow or overflow outside of an unchecked block.",
        0x12: "Divide or modulo operation by zero.",
        0x21: "Convert a value that is too big or negative into an enum type.",
        0x22: "Access a storage byte array that is incorrectly encoded.",
        0x31: "Call .pop() on an empty array.",
        0x32: "Access an array, bytesN or an array slice at an out-of-bounds or negative index.",
        0x41: "Allocate too much memory or create an array that is too large.",
        0x51: "Call a zero-initialized variable of internal function type.",
    }

    def __init__(self, config: ConfigManager, abi_path: Path | None = None, log_level: int = logging.INFO) -> None:
        """
        Initialize the CustomErrorParser with the ABI file path and load the ABI.

        :param config: Configuration manager for the blockchain connection.
        :param abi_path: Path to the ABI JSON file. Defaults to '../contracts/errors.json' if not provided.
        :param log_level: Logging level for this class (default: logging.INFO).
        """
        self.config = config
        self._abi_path = abi_path or Path(__file__).parent / self.config.contracts.errors.abi_path
        self._abi = self._load_abi_from_file()
        self._interface: Type[Contract] = self.config.connection.eth.contract(abi=self._abi)

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

    def _load_abi_from_file(self) -> list[dict[str, Any]]:
        """
        Load the ABI from a JSON file.

        :return: A list representing the ABI from the JSON file.
        :raises Exception: If the file is not found, JSON parsing fails, or the ABI key is missing.
        """
        try:
            with open(self._abi_path, "r") as file:
                data = json.load(file)
                abi = data.get("abi")
                if not abi:
                    raise KeyError("ABI key not found.")
                return abi
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Error loading ABI from {self._abi_path}: {e}")
            raise Exception(f"Error loading ABI from {self._abi_path}: {e}")

    def _parse_custom_error(self, error_bytes: str) -> dict[str, Any] | None:
        """
        Attempt to parse a custom Solidity error using the provided error bytes and ABI.

        :param error_bytes: The error bytes returned from a transaction.
        :return: Parsed error information or None if no match is found.
        """
        err_fnc_hash = error_bytes[:10]  # First 4 bytes are the function selector
        for item in self._abi:
            function_definition = f"{item['name']}(" + ",".join([inpt["type"] for inpt in item["inputs"]]) + ")"
            fc_hash = keccak(text=function_definition).hex()
            param_names = [inpt["name"] for inpt in item["inputs"]]

            # Compare the first 4 bytes of the hash with the error's function selector
            if ("0x" + fc_hash)[:10] == err_fnc_hash:
                self.logger.info(f"Matched function: {item['name']}")
                encoded_data = error_bytes[10:]
                decoded_vals = decode([inpt["type"] for inpt in item["inputs"]], decode_hex(encoded_data))
                return {
                    "function_name": item["name"],
                    "function_selector": ("0x" + fc_hash)[:10],
                    "function_definition": function_definition,
                    "function_hash": fc_hash,
                    "param_names": param_names,
                    "param_vals": decoded_vals,
                }
        return None

    def _parse_panic(self, error_bytes: str) -> dict[str, Any] | None:
        """
        Attempt to parse a Panic(uint256) error.

        :param error_bytes: The error bytes returned from a transaction.
        :return: Parsed panic message and code if matched.
        """
        panic_signature: str = ("0x" + keccak(text="Panic(uint256)").hex())[:10]
        if error_bytes.startswith(panic_signature):
            panic_code_bytes: str = error_bytes[len(panic_signature) :]
            panic_code: int = decode(["uint256"], decode_hex(panic_code_bytes))[0]
            panic_message = self.PANIC_MAP.get(panic_code, "Unknown panic code")
            self.logger.info(f"Parsed Panic({hex(panic_code)}): {panic_message}")
            return {
                "panic": panic_message,
                "panic_code": panic_code,
                "hex_panic_code": hex(panic_code),
            }
        return None

    def _parse_error_string(self, error_bytes: str) -> dict[str, Any] | None:
        """
        Attempt to parse a standard Error(string) error.

        :param error_bytes: The error bytes returned from a transaction.
        :return: Parsed error string if matched.
        """
        error_signature: str = ("0x" + keccak(text="Error(string)").hex())[:10]
        if error_bytes.startswith(error_signature):
            error_string_bytes: str = error_bytes[len(error_signature) :]
            error_string: str = decode(["string"], decode_hex(error_string_bytes))[0]
            self.logger.info(f'Parsed Error("{error_string}")')
            return {"error": error_string}
        return None

    def _parse_generic_string(self, error_bytes: str) -> dict[str, Any]:
        """
        Attempt to parse the error as a generic string, as a last fallback option.

        :param error_bytes: The error bytes returned from a transaction.
        :return: Parsed string if valid, or unknown error message if parsing fails.
        """
        try:
            parsed_string: str = decode_hex(error_bytes).decode()
            self.logger.info(f"Parsed string: {parsed_string}")
            return {"String": parsed_string}
        except Exception as e:
            self.logger.error(f"Unable to parse error reason: {e}")
            return {"Unknown": "Unable to parse error reason."}

    def parse_error(self, error_bytes: str, should_throw: bool = True) -> dict[str, Any]:
        """
        Parse the custom error from the error bytes and match it with the ABI or standard errors.

        :param error_bytes: The error bytes returned from a transaction.
        :param should_throw: Whether to throw an exception if parsing fails. Defaults to True.
        :return: Parsed error information or a fallback message.
        :raises Exception: If no matching function signature is found or decoding fails.
        """
        try:
            error_bytes = error_bytes.lower()
            if not error_bytes.startswith("0x"):
                error_bytes = "0x" + error_bytes

            # Attempt to parse a custom error
            custom_result: dict[str, Any] | None = self._parse_custom_error(error_bytes)
            if custom_result:
                return custom_result

            # Fallback to Panic or Error(string)
            panic_result: dict[str, Any] | None = self._parse_panic(error_bytes)
            if panic_result:
                return panic_result

            error_string_result: dict[str, Any] | None = self._parse_error_string(error_bytes)
            if error_string_result:
                return error_string_result

            # Fallback: Try parsing as a generic string
            return self._parse_generic_string(error_bytes)

        except Exception as e:
            # Fallback for unknown errors
            self.logger.error(f"Could not parse error_bytes {error_bytes}: {e}")
            if should_throw:
                raise Exception(f"Unknown error: Could not parse error_bytes {error_bytes}")
            return {"Unknown": "Unable to parse error reason."}

    @staticmethod
    def get_error_string(error_reason: dict[str, Any]) -> str:
        """
        Convert the parsed error into a readable string format.

        :param error_reason: Parsed error information, including function name and parameters.
        :return: A JSON-formatted string representing the parsed error.
        """
        try:
            return json.dumps(
                {
                    "name": error_reason["function_name"],
                    "function_selector": error_reason["function_selector"],
                    "function_definition": error_reason["function_definition"],
                    "args": {n: v for n, v in zip(error_reason["param_names"], error_reason["param_vals"])},
                }
            )
        except KeyError:
            return json.dumps({"Error": error_reason})

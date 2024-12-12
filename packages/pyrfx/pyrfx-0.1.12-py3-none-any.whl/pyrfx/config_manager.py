import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from web3 import Web3
from web3.types import ChecksumAddress


@dataclass
class ContractInfo:
    """
    Represents the information for a smart contract, including its address and the path to its ABI.
    """

    contract_address: ChecksumAddress
    abi_path: str


@dataclass
class NetworkContracts:
    """
    Holds contract information for various contract types within a given blockchain network.
    """

    data_store: ContractInfo
    event_emitter: ContractInfo
    exchange_router: ContractInfo
    deposit_vault: ContractInfo
    withdrawal_vault: ContractInfo
    order_vault: ContractInfo
    reader: ContractInfo
    router: ContractInfo
    errors: ContractInfo
    referral_storage: ContractInfo

    def __getitem__(self, contract_name: str) -> ContractInfo | None:
        """
        Allow dictionary-style access to the contracts by contract name.

        :param contract_name: The name of the contract to access (e.g., 'data_store', 'event_emitter').
        :return: The ContractInfo associated with the contract name or None if not found.
        """
        return getattr(self, contract_name, None)


# Default chain configurations
DEFAULT_CHAINS: Final[dict[str, dict[str, str | int]]] = {
    "zkSync": {
        "rpc_url": "https://mainnet.era.zksync.io",
        "chain_id": 324,
        "block_explorer_url": "https://era.zksync.network",
        "oracle_url": "https://k5npgabr92.execute-api.us-east-1.amazonaws.com/signed_prices/latest",
        "tokens_url": "https://k5npgabr92.execute-api.us-east-1.amazonaws.com/tokens",
        # https://explorer.zksync.io/address/0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91
        "weth_address": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        # USDC.e bridged: https://explorer.zksync.io/address/0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4
        "usdc_address": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
    },
    "zkSyncInternal": {
        "rpc_url": "https://mainnet.era.zksync.io",
        "chain_id": 324,
        "block_explorer_url": "https://era.zksync.network",
        "oracle_url": "https://k5npgabr92.execute-api.us-east-1.amazonaws.com/signed_prices/latest",
        "tokens_url": "https://k5npgabr92.execute-api.us-east-1.amazonaws.com/tokens",
        # https://explorer.zksync.io/address/0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91
        "weth_address": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        # USDC.e bridged: https://explorer.zksync.io/address/0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4
        "usdc_address": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
    },
    "zkSyncSepolia": {
        "rpc_url": "https://sepolia.era.zksync.dev/rpc",
        "chain_id": 300,
        "block_explorer_url": "https://sepolia-era.zksync.network",
        "oracle_url": "https://k5npgabr92.execute-api.us-east-1.amazonaws.com/signed_prices/latest",
        "tokens_url": "https://k5npgabr92.execute-api.us-east-1.amazonaws.com/tokens",
        # https://sepolia.explorer.zksync.io/address/0x138DCa29f0dF3492bce88f1E897a23b04c161913
        "weth_address": "0x138DCa29f0dF3492bce88f1E897a23b04c161913",
        # https://sepolia.explorer.zksync.io/address/0x9B2bcE861E8455AD88eaBAD7C73ce96edD663C7c
        "usdc_address": "0x9B2bcE861E8455AD88eaBAD7C73ce96edD663C7c",
    },
}

CONTRACT_MAP: Final[dict[str, dict[str, dict[str, str]]]] = {
    "zkSync": {
        "data_store": {
            "contract_address": "0x895124783008C6c68eFcccac24c482Fdf30439B2",
            "abi_path": "contracts/zksync/data_store.json",
        },
        "event_emitter": {
            "contract_address": "0x9F006F3a4177e645Fc872B911Cf544E890c82B1A",
            "abi_path": "contracts/zksync/event_emitter.json",
        },
        "exchange_router": {
            "contract_address": "0x36F6469B33c2cAE33beC387852062413BBA70262",
            "abi_path": "contracts/zksync/exchange_router.json",
        },
        "deposit_vault": {
            "contract_address": "0x252e8f48694b2ec03A92eef298F986A7b5cE3B71",
            "abi_path": "contracts/zksync/deposit_vault.json",
        },
        "withdrawal_vault": {
            "contract_address": "0xe62d220DEF5d1656447289fA001cFc69a8Af1fb7",
            "abi_path": "contracts/zksync/withdrawal_vault.json",
        },
        "order_vault": {
            "contract_address": "0x21150394A988FD88b18492611df005372cAe998D",
            "abi_path": "contracts/zksync/order_vault.json",
        },
        "reader": {
            "contract_address": "0x25A5cFB62a7461a3EEEC6e076DE522521298511b",
            "abi_path": "contracts/zksync/reader.json",
        },
        "router": {
            "contract_address": "0xd06a1fA35C92281c5F8F00450d29180FCA7e98C1",
            "abi_path": "contracts/zksync/router.json",
        },
        "errors": {
            "contract_address": "0x0000000000000000000000000000000000000000",
            "abi_path": "contracts/zksync/errors.json",
        },
        "referral_storage": {
            "contract_address": "0xEc7bad664e0dD84348c38f229F56c865Ec49AA23",
            "abi_path": "contracts/zksync/referral_storage.json",
        },
    },
    "zkSyncInternal": {
        "data_store": {
            "contract_address": "0x4F6beE9Bc2562df95e1A1D55e48D70a00DBB3379",
            "abi_path": "contracts/zksync_internal/data_store.json",
        },
        "event_emitter": {
            "contract_address": "0x850c4603e46feB6Dd13c16B638Bf2CB7c520f75A",
            "abi_path": "contracts/zksync_internal/event_emitter.json",
        },
        "exchange_router": {
            "contract_address": "0x1404a9a7aF54c01b4a205330Ca91aA434e08AC83",
            "abi_path": "contracts/zksync_internal/exchange_router.json",
        },
        "deposit_vault": {
            "contract_address": "0x1717B74EfB03303c82451f1a3A38cE06E3f30Cb3",
            "abi_path": "contracts/zksync_internal/deposit_vault.json",
        },
        "withdrawal_vault": {
            "contract_address": "0x847A2cC2bE438A25117843e4a890569e02f1f20F",
            "abi_path": "contracts/zksync_internal/withdrawal_vault.json",
        },
        "order_vault": {
            "contract_address": "0xbA1c8d37fF92377Be2B0731982DB0003A37AC2C2",
            "abi_path": "contracts/zksync_internal/order_vault.json",
        },
        "reader": {
            "contract_address": "0x71384FE85F5bbDb1C3de9DdAE05eCe456f18Fe5b",
            "abi_path": "contracts/zksync_internal/reader.json",
        },
        "router": {
            "contract_address": "0xF028b432cB1012e6dE5D1b3D81D77f5059DDb3d8",
            "abi_path": "contracts/zksync_internal/router.json",
        },
        "errors": {
            "contract_address": "0x0000000000000000000000000000000000000000",
            "abi_path": "contracts/zksync_internal/errors.json",
        },
        "referral_storage": {
            "contract_address": "0x4669588Cd48Df1017A170b215bf1731c85455Db1",
            "abi_path": "contracts/zksync_internal/referral_storage.json",
        },
    },
    "zkSyncSepolia": {
        "data_store": {
            "contract_address": "0xD5a9c50e65eBcF20DF8Df7d3f0D825D8202EBEfc",
            "abi_path": "contracts/zksync_sepolia/data_store.json",
        },
        "event_emitter": {
            "contract_address": "0x2011E4372D681AEB2B62DBFe9806b0C6c963eE1c",
            "abi_path": "contracts/zksync_sepolia/event_emitter.json",
        },
        "exchange_router": {
            "contract_address": "0xa64a7FdD8ab84157172a781691380316010204A3",
            "abi_path": "contracts/zksync_sepolia/exchange_router.json",
        },
        "deposit_vault": {
            "contract_address": "0x1B8CB84caC7fbAb848670B331f49759C3c1d976f",
            "abi_path": "contracts/zksync_sepolia/deposit_vault.json",
        },
        "withdrawal_vault": {
            "contract_address": "0xC3A463123eF29Fab3b0935889ADd502B38CbB9aC",
            "abi_path": "contracts/zksync_sepolia/withdrawal_vault.json",
        },
        "order_vault": {
            "contract_address": "0x964163A7b0F4C0E36F6684786261B786Ae4090c4",
            "abi_path": "contracts/zksync_sepolia/order_vault.json",
        },
        "reader": {
            "contract_address": "0xD9c04c3d2258438f8E38381E61e854f6dC8Caea2",
            "abi_path": "contracts/zksync_sepolia/reader.json",
        },
        "router": {
            "contract_address": "0x38f2543e8c6C6954E71fA1cAa2eb9d39fBE64107",
            "abi_path": "contracts/zksync_sepolia/router.json",
        },
        "errors": {
            "contract_address": "0x0000000000000000000000000000000000000000",
            "abi_path": "contracts/zksync_sepolia/errors.json",
        },
        "referral_storage": {
            "contract_address": "0x63B333b0f5c2c90B727A300663b43C4182194671",
            "abi_path": "contracts/zksync_sepolia/referral_storage.json",
        },
    },
}


class ConfigManager:
    """
    Manages configuration settings such as RPC URLs, wallet addresses, and chain information.
    """

    def __init__(
        self,
        chain: str = "zkSync",
        rpc_url: str | None = None,
        chain_id: int | None = None,
        block_explorer_url: str | None = None,
        oracle_url: str | None = None,
        tokens_url: str | None = None,
        user_wallet_address: ChecksumAddress | str | None = None,
        private_key: str | None = None,
        save_to_json: bool = False,
        save_to_csv: bool = False,
        output_data_folder: Path | str | None = None,
    ) -> None:
        """
        Initializes the ConfigManager with the given blockchain network configuration.

        :param chain: The blockchain network name (e.g., 'zkSync', 'zkSyncSepolia').
        :param rpc_url: Optional RPC URL for interacting with the blockchain.
        :param chain_id: Optional chain ID for the blockchain network.
        :param block_explorer_url: Optional block explorer URL for the blockchain.
        :param oracle_url: Optional oracle URL for the blockchain.
        :param tokens_url: Optional tokens URL for the blockchain.
        :param user_wallet_address: Optional wallet address of the user.
        :param private_key: Optional private key associated with the wallet.
        :param save_to_json: Optional boolean flag indicating whether to save outputs to JSON.
        :param save_to_csv: Optional boolean flag indicating whether to save outputs to CSV.
        :param output_data_folder: Optional output data folder path.
        """
        self.chain: Final[str] = chain

        # Set defaults from known chains
        defaults: dict[str, str | int] = DEFAULT_CHAINS.get(chain)
        if not defaults:
            raise ValueError(f"No chain info was found for chain: {chain}")

        # Use a generic initializer method
        self.rpc_url: Final[str] = self._get_value(rpc_url, defaults, "rpc_url")
        self.chain_id: Final[int] = self._get_value(chain_id, defaults, "chain_id")
        self.block_explorer_url: Final[str] = self._get_value(block_explorer_url, defaults, "block_explorer_url")
        self.oracle_url: Final[str] = self._get_value(oracle_url, defaults, "oracle_url")
        self.tokens_url: Final[str] = self._get_value(tokens_url, defaults, "tokens_url")

        # Set up blockchain connection
        self.connection: Final[Web3] = Web3(Web3.HTTPProvider(self.rpc_url))
        self.contracts: Final[NetworkContracts] = self._initialize_chain_contracts()

        # Wallet and private key handling
        self.user_wallet_address: ChecksumAddress = self._initialize_wallet_address(user_wallet_address)
        self.private_key: str = self._initialize_private_key(private_key)

        # Storage flags and output data folder
        self.save_to_json: bool = save_to_json
        self.save_to_csv: bool = save_to_csv
        if output_data_folder:
            self.data_path: Path = (
                output_data_folder if isinstance(output_data_folder, Path) else Path(output_data_folder)
            )
        else:
            self.data_path = None
        if (self.save_to_json or self.save_to_csv) and self.data_path is None:
            logging.error("No data path was specified.")
            raise ValueError("No data path was specified.")

        # Set well-known addresses
        self.weth_address: ChecksumAddress = self.to_checksum_address(defaults.get("weth_address"))
        self.usdc_address: ChecksumAddress = self.to_checksum_address(defaults.get("usdc_address"))
        self.zero_address: ChecksumAddress = self.to_checksum_address("0x0000000000000000000000000000000000000000")

    @staticmethod
    def _get_value(provided_value: Any, defaults: dict[str, Any], key: str) -> Any:
        """
        Retrieve a value either from provided arguments or from defaults.

        :param provided_value: The value provided during initialization.
        :param defaults: A dictionary containing default chain configuration values.
        :param key: The key to look up in the defaults if the provided value is None.
        :return: The value for the given key, either provided or from defaults.
        :raises ValueError: If neither the provided value nor a default is available.
        """
        value: Any = provided_value or defaults.get(key)
        if value is None:
            logging.error(f"No value was specified for {key}.")
            raise ValueError(f"No value was specified for {key}.")
        return value

    def _initialize_chain_contracts(self) -> NetworkContracts:
        """
        Initializes the contract information for the selected chain, converting addresses to checksum format.

        :return: The initialized NetworkContracts object containing contract addresses and ABI paths.
        :raises ValueError: If no chain contracts are found for the specified chain.
        """
        chain_contracts: dict[str, dict[str, str]] | None = CONTRACT_MAP.get(self.chain)
        if not chain_contracts:
            logging.error(f"No chain contracts were found for chain: {self.chain}")
            raise ValueError(f"No chain contracts were found for chain: {self.chain}")

        return NetworkContracts(
            **{
                contract_name: ContractInfo(
                    contract_address=self.to_checksum_address(info["contract_address"]),
                    abi_path=info["abi_path"],
                )
                for contract_name, info in chain_contracts.items()
            }
        )

    def to_checksum_address(self, address: str) -> ChecksumAddress:
        """
        Converts an address to checksum format.

        :param address: The address to convert.
        :return: The checksummed address.
        """
        return self.connection.to_checksum_address(address)

    def _initialize_wallet_address(self, user_wallet_address: str | None) -> ChecksumAddress:
        """
        Initializes the user wallet address, either from the provided argument or environment variables.

        :param user_wallet_address: Optional user wallet address. If not provided, fetches from environment variables.
        :return: The checksummed wallet address.
        :raises ValueError: If no wallet address is provided or found in environment variables.
        """
        user_wallet_address: str = user_wallet_address or os.getenv("USER_WALLET_ADDRESS")
        if not user_wallet_address:
            logging.error("No user wallet address was specified.")
            raise ValueError("User wallet address not provided.")
        return self.to_checksum_address(user_wallet_address)

    @staticmethod
    def _initialize_private_key(private_key: str | None) -> str:
        """
        Initializes the private key, either from the provided argument or environment variables.

        :param private_key: The private key.
        :return: The initialized private key.
        :raises ValueError: If no private key is provided or found in environment variables.
        """
        private_key: str = private_key or os.getenv("PRIVATE_KEY")
        if not private_key:
            logging.error("No private key was specified.")
            raise ValueError("Private key not provided.")
        return private_key

    def __repr__(self) -> str:
        """
        Returns a string representation of the ConfigManager object, masking sensitive information.

        :return: A string representation of the ConfigManager.
        """
        return (
            f"ConfigManager(chain={self.chain}, "
            f"rpc_url={self.rpc_url}, "
            f"user_wallet_address={self.user_wallet_address}, "
            f"private_key={'<hidden>' if self.private_key else 'None'})"
        )

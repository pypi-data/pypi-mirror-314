import json
import logging
from logging import Logger
from pathlib import Path

from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3.contract import Contract
from web3.types import ChecksumAddress, TxParams

from pyrfx.config_manager import ConfigManager


def check_if_approved(
    config: ConfigManager,
    spender_address: str | ChecksumAddress,
    token_to_approve_address: str | ChecksumAddress,
    max_fee_per_gas: int,
    approve: bool = True,
    amount_of_tokens_to_approve_to_spend: int | None = None,
    logger: Logger | None = None,
) -> None:
    """
    Check if a given amount of tokens is approved for spending by a contract, and approve if necessary.

    :param config: The configuration object containing network and user details.
    :param spender_address: The contract address of the requested spender.
    :param token_to_approve_address: The contract address of the token to spend.
    :param max_fee_per_gas: The maximum fee per gas to be used for the transaction.
    :param approve: Set to True if you want to approve spending if not already approved.
    :param amount_of_tokens_to_approve_to_spend: The amount of tokens to approve to spend, in expanded decimals.
    :param logger: The logger object.

    :raises Exception: If there is an insufficient balance or the token is not approved for spending.
    :return: None.
    """
    if not amount_of_tokens_to_approve_to_spend:
        # Max uint
        amount_of_tokens_to_approve_to_spend: int = 2**256 - 1

    if not logger:
        logger: Logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

    # Convert addresses to checksum format
    if not config.connection.is_checksum_address(spender_address):
        spender_address: ChecksumAddress = config.to_checksum_address(address=spender_address)
    if not config.connection.is_checksum_address(token_to_approve_address):
        token_to_approve_address: ChecksumAddress = config.to_checksum_address(address=token_to_approve_address)
    user_wallet_address: str | ChecksumAddress | None = config.user_wallet_address
    if not config.connection.is_checksum_address(user_wallet_address):
        user_wallet_address: ChecksumAddress = config.to_checksum_address(address=user_wallet_address)

    # Load ABI for the token contract
    file_path: Path = Path(__file__).parent / "contracts" / "token_approval.json"

    # Check if the file exists before trying to open it
    if file_path.exists():
        with file_path.open() as file:
            token_contract_abi: dict = json.load(file)
    else:
        logger.error(f"The file {file_path} does not exist.")
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    token_contract_obj: Contract = config.connection.eth.contract(
        address=token_to_approve_address, abi=token_contract_abi
    )

    # Check the amount already approved for the spender
    amount_approved: int = token_contract_obj.functions.allowance(user_wallet_address, spender_address).call()

    logger.info("Checking if tokens are already approved for spending ...")

    # If the tokens are not approved and approval is requested, approve them
    if amount_approved < amount_of_tokens_to_approve_to_spend and approve:
        if amount_of_tokens_to_approve_to_spend == 2**256 - 1:
            logger.info(
                f'Approving contract "{spender_address}" to spend maximum uint (2^256-1) '
                f"tokens belonging to token address: {token_to_approve_address}"
            )
        else:
            logger.info(
                f'Approving contract "{spender_address}" to spend {amount_of_tokens_to_approve_to_spend} '
                f"tokens belonging to token address: {token_to_approve_address}"
            )

        nonce: int = config.connection.eth.get_transaction_count(user_wallet_address)

        # Build the transaction to approve token spending
        raw_txn: TxParams = token_contract_obj.functions.approve(
            spender_address, amount_of_tokens_to_approve_to_spend
        ).build_transaction(
            {
                "value": 0,
                "chainId": config.chain_id,
                "gas": 500_000,
                "maxFeePerGas": int(max_fee_per_gas),
                "maxPriorityFeePerGas": 0,
                "nonce": nonce,
            }
        )

        # Sign the transaction with the user's private key
        signed_txn: SignedTransaction = config.connection.eth.account.sign_transaction(raw_txn, config.private_key)
        tx_hash: HexBytes = config.connection.eth.send_raw_transaction(signed_txn.raw_transaction)

        tx_url: str = f"{config.block_explorer_url}/tx/0x{tx_hash.hex()}"
        logger.info(f"Transaction submitted! Transaction hash: 0x{tx_hash.hex()}")
        logger.info(f"Transaction submitted! Check status: {tx_url}")

    # If tokens are not approved but approval is not requested, raise an exception
    elif amount_approved < amount_of_tokens_to_approve_to_spend and not approve:
        raise Exception("Token not approved for spend, please allow first!")

    # If tokens are already approved or successfully approved, print confirmation
    if amount_of_tokens_to_approve_to_spend == 2**256 - 1:
        logger.info(
            f'Contract "{spender_address}" approved to spend maximum uint (2^256-1) '
            f"tokens belonging to token address: {token_to_approve_address}"
        )
    else:
        logger.info(
            f'Contract "{spender_address}" approved to spend {amount_of_tokens_to_approve_to_spend} '
            f"tokens belonging to token address: {token_to_approve_address}"
        )
    logger.info("Tokens approved for spending!")

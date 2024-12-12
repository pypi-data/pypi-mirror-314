import logging
from typing import Any

from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.get.pool_tvl import PoolTVL
from pyrfx.order.arg_parser_order import OrderArgumentParser
from pyrfx.order.swap_router import SwapRouter
from pyrfx.utils import get_available_tokens, get_estimated_swap_output


class EstimateSwapOutput:
    """
    A class to estimate swap output.
    """

    def __init__(
        self, config: ConfigManager, markets: dict[ChecksumAddress, dict[str, Any]], log_level: int = logging.INFO
    ) -> None:
        """
        Initialize the EstimateSwapOutput class with a configuration object and self.logger.

        :param config: ConfigManager object containing chain configuration.
        :param log_level: Logging level for the logger.
        """
        self.config: ConfigManager = config

        # Setup logger
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.markets: dict[ChecksumAddress, dict[str, Any]] = markets
        self.tokens: dict[ChecksumAddress, dict[str, ChecksumAddress | int | bool]] = get_available_tokens(
            config=self.config
        )

    def get_swap_output(
        self,
        start_token_symbol: str,
        out_token_symbol: str,
        token_amount: float,
        start_token_address: ChecksumAddress | None = None,
        out_token_address: ChecksumAddress | None = None,
        token_amount_expanded: float | None = None,
    ):
        """
        Estimate swap output for a given input token and amount.

        :param start_token_symbol: The symbol of the input token (e.g., "WETH"). Default is None.
        :param out_token_symbol: The symbol of the output token (e.g., "USDC"). Default is None.
        :param token_amount: Amount of tokens in human-readable format (e.g., 1 = one token). Default is None.
        :param start_token_address: Contract address of the input token. Default is None.
        :param out_token_address: Contract address of the output token. Default is None.
        :param token_amount_expanded: Expanded token amount (e.g., 1 BTC = 10000000). Default is None.
        :return: Dictionary with the amount of output tokens and price impact in USD.
        """
        try:
            # Resolve input token address
            if start_token_address is None:
                oap: OrderArgumentParser = OrderArgumentParser(config=self.config, operation_type="increase")
                start_token_address: ChecksumAddress = self.config.to_checksum_address(
                    oap.find_key_by_symbol(input_dict=self.tokens, search_symbol=start_token_symbol)
                )
                self.logger.info(f"Resolved in_token_address for {start_token_symbol}: {start_token_address}")

            # Resolve output token address
            if out_token_address is None:
                oap: OrderArgumentParser = OrderArgumentParser(config=self.config, operation_type="increase")
                out_token_address: ChecksumAddress = self.config.to_checksum_address(
                    oap.find_key_by_symbol(input_dict=self.tokens, search_symbol=out_token_symbol)
                )
                self.logger.info(f"Resolved out_token_address for {out_token_symbol}: {out_token_address}")

            # Expand token amount if not provided
            if token_amount_expanded is None:
                token_amount_expanded: int = int(token_amount * 10 ** self.tokens[start_token_address]["decimals"])
                self.logger.info(f"Expanded token amount for {start_token_symbol}: {token_amount_expanded}")

            # Determine the swap route
            pool_tvl: dict[str, dict[str, Any]] = PoolTVL(config=self.config).get_pool_balances()
            swap_router: SwapRouter = SwapRouter(config=self.config, pool_tvl=pool_tvl)
            swap_route: list[ChecksumAddress] = swap_router.determine_swap_route(
                available_markets=self.markets,
                in_token_address=start_token_address,
                out_token_address=out_token_address,
            )
            self.logger.info(f"Swap route determined: {swap_route}")

            # TODO: Implement estimate swap output for 2 step swap: token -> USDC -> token
            # Estimate the output of the swap
            output: dict[str, float] = self.estimated_swap_output(
                market=self.markets[swap_route[0]],
                in_token=start_token_address,
                token_amount_expanded=token_amount_expanded,
            )
            self.logger.info(f"Estimated swap output: {output}")

            # Convert output token amount back to human-readable format
            output["out_token_actual"] = output["out_token_amount"] / 10 ** self.tokens[out_token_address]["decimals"]
            output["price_impact"] = output["price_impact_usd"] / 10**18

            return output

        except Exception as e:
            self.logger.error(f"An error occurred while estimating swap output: {e}")
            raise

    def estimated_swap_output(self, market: dict, in_token: str, token_amount_expanded: int) -> dict[str, float]:
        """
        Estimate the swap output for a given market, input token, and amount.

        :param market: Details of the market to swap through.
        :param in_token: Contract address of the input token.
        :param token_amount_expanded: Expanded amount of tokens to swap.
        :return: Dictionary with the amount of output tokens and price impact in USD.
        """
        try:
            prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

            token_addresses: list[str] = [
                market["index_token_address"],
                market["long_token_address"],
                market["short_token_address"],
            ]

            # Fetch prices for the relevant tokens
            token_prices: list[list[int]] = [
                [int(prices[token]["maxPriceFull"]), int(prices[token]["minPriceFull"])] for token in token_addresses
            ]

            # Prepare parameters for the estimated swap output
            estimated_swap_output_parameters: dict[str, Any] = {
                "data_store_address": self.config.contracts.data_store.contract_address,
                "market_addresses": [market["rfx_market_address"]] + token_addresses,
                "token_prices_tuple": token_prices,
                "token_in": self.config.to_checksum_address(in_token),
                "token_amount_in": token_amount_expanded,
                "ui_fee_receiver": self.config.zero_address,
            }

            self.logger.info(estimated_swap_output_parameters)

            # Get the estimated swap output
            return get_estimated_swap_output(self.config, estimated_swap_output_parameters)

        except KeyError as ke:
            self.logger.error(f"Missing price data for token: {ke}")
            raise
        except Exception as e:
            self.logger.error(f"An error occurred during swap output estimation: {e}")
            raise

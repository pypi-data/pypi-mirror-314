import logging
from logging import Logger
from typing import Any

from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager


class SwapRouter:
    """
    A class to determine optimal swap routes for token swaps, using either a direct one-hop route or a
    two-hop route via USDC as an intermediary token.
    """

    def __init__(
        self, config: ConfigManager, pool_tvl: dict[str, dict[str, Any]], log_level: int = logging.INFO
    ) -> None:
        """
        Initialize the SwapRouter with configuration settings and TVL data for available pools.

        :param config: Configuration manager with essential settings like USDC address.
        :param pool_tvl: Dictionary containing TVL information for each pool, indexed by market addresses.
        :param log_level: Logging level for the SwapRouter's logger.
        """
        self.config: ConfigManager = config
        self.pool_tvl: dict[str, dict[str, Any]] = pool_tvl
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

    def determine_swap_route(
        self,
        available_markets: dict[ChecksumAddress, dict],
        in_token_address: ChecksumAddress,
        out_token_address: ChecksumAddress,
    ) -> list[ChecksumAddress]:
        """
        Find the list of RFX markets required to swap from one token to another.
        If a two-step swap is required, it automatically assumes USDC as the intermediate token.

        :param available_markets: Dictionary of available markets.
        :param in_token_address: The address of the input token.
        :param out_token_address: The address of the output token.
        :return: A tuple containing the list of RFX markets and a boolean indicating if multi-swap is required.
        :raises ValueError: If no swap route is available.
        """
        if in_token_address == out_token_address:
            self.logger.error(f"Input token and output token are the same: {in_token_address}")
            raise ValueError("Input token and output token must be different.")

        try:
            # One-hop route
            one_hop_route = self._find_one_hop_route(available_markets, in_token_address, out_token_address)
            if one_hop_route:
                return [one_hop_route]
        except ValueError:
            self.logger.debug("No one-hop route found, trying two-hop route.")

        try:
            # Two-hop route
            two_hop_route = self._find_two_hop_route(available_markets, in_token_address, out_token_address)
            if two_hop_route:
                return two_hop_route
        except ValueError:
            self.logger.debug("No two-hop route found.")

        # If no routes are found
        self.logger.error(f"No available swap route from {in_token_address} to {out_token_address}")
        raise ValueError("No available swap route.")

    def _find_one_hop_route(
        self,
        available_markets: dict[ChecksumAddress, dict],
        in_token_address: ChecksumAddress,
        out_token_address: ChecksumAddress,
    ) -> ChecksumAddress | None:
        """
        Find the best one-hop route based on TVL from available markets.

        :param available_markets: Dictionary of available markets.
        :param in_token_address: The address of the input token.
        :param out_token_address: The address of the output token.
        :return: The address of the RFX market selected for the one-hop route, or None if no route found.
        :raises ValueError: If no direct route is available.
        """
        best_market_address: ChecksumAddress | None = None
        highest_tvl: float = 0.0
        selected_market_metadata: dict | None = None

        # Find the best market with the highest TVL
        for market_metadata in available_markets.values():
            if (
                market_metadata["long_token_address"] == in_token_address
                and market_metadata["short_token_address"] == out_token_address
            ) or (
                market_metadata["short_token_address"] == in_token_address
                and market_metadata["long_token_address"] == out_token_address
            ):
                market_address = self.config.to_checksum_address(market_metadata["rfx_market_address"])
                tvl = self.pool_tvl.get(market_address, {}).get("tvl_total", 0.0)

                if tvl > highest_tvl:
                    best_market_address: ChecksumAddress = market_address
                    highest_tvl: float = tvl
                    # Store the selected market metadata
                    selected_market_metadata: dict = market_metadata

        # Log details for the market with the highest TVL
        if best_market_address and selected_market_metadata:
            long_symbol = selected_market_metadata["long_token_metadata"]["symbol"]
            short_symbol = selected_market_metadata["short_token_metadata"]["symbol"]
            market_symbol = selected_market_metadata["market_symbol"]
            self.logger.info(
                f"Direct swap found, pool '{market_symbol}': "
                f"{long_symbol} –> {short_symbol} "
                f"({in_token_address} -> {out_token_address}), TVL: ${highest_tvl:,.2f}"
            )
            return best_market_address

        self.logger.error(f"No direct swap route found for tokens: {in_token_address} -> {out_token_address}")
        return None

    def _find_two_hop_route(
        self,
        available_markets: dict[ChecksumAddress, dict],
        in_token_address: ChecksumAddress,
        out_token_address: ChecksumAddress,
    ) -> list[ChecksumAddress] | None:
        """
        Find the best two-hop route from `in_token_address` to `out_token_address` using USDC as an intermediate token.

        :param available_markets: Dictionary of available markets.
        :param in_token_address: The address of the input token.
        :param out_token_address: The address of the output token.
        :return: A list containing the RFX market addresses for each hop in the two-hop route, or None if no route
            found.
        :raises ValueError: If no suitable two-hop route is available.
        """
        best_step1_market_address: ChecksumAddress | None = None
        best_step2_market_address: ChecksumAddress | None = None
        highest_tvl: float = 0.0
        selected_step1_metadata: dict | None = None
        selected_step2_metadata: dict | None = None

        # Step 1: Find best market from in_token -> USDC
        for market_metadata in available_markets.values():
            if (
                market_metadata["long_token_address"] == in_token_address
                and market_metadata["short_token_address"] == self.config.usdc_address
            ):
                step1_market_address = self.config.to_checksum_address(market_metadata["rfx_market_address"])
                step1_tvl = self.pool_tvl.get(step1_market_address, {}).get("tvl_total", 0.0)

                # Step 2: Find best market from USDC -> out_token
                for step2_metadata in available_markets.values():
                    if (
                        step2_metadata["long_token_address"] == self.config.usdc_address
                        and step2_metadata["short_token_address"] == out_token_address
                    ):
                        step2_market_address = self.config.to_checksum_address(step2_metadata["rfx_market_address"])
                        step2_tvl = self.pool_tvl.get(step2_market_address, {}).get("tvl_total", 0.0)
                        total_tvl = step1_tvl + step2_tvl

                        if total_tvl > highest_tvl:
                            best_step1_market_address: ChecksumAddress = step1_market_address
                            best_step2_market_address: ChecksumAddress = step2_market_address
                            highest_tvl: float = total_tvl
                            selected_step1_metadata: dict = market_metadata
                            selected_step2_metadata: dict = step2_metadata

        # Log details for the best two-hop route with TVL for each hop
        if (
            best_step1_market_address
            and best_step2_market_address
            and selected_step1_metadata
            and selected_step2_metadata
        ):
            start_symbol = selected_step1_metadata["long_token_metadata"]["symbol"]
            end_symbol = selected_step2_metadata["short_token_metadata"]["symbol"]
            step1_tvl = self.pool_tvl[best_step1_market_address]["tvl_total"]
            step2_tvl = self.pool_tvl[best_step2_market_address]["tvl_total"]
            self.logger.info(
                f"Two-step swap required: "
                f"{start_symbol} -> USDC -> {end_symbol} "
                f"({in_token_address} -> {self.config.usdc_address} -> {out_token_address}), "
                f"Step 1 TVL: ${step1_tvl:,.2f}, Step 2 TVL: ${step2_tvl:,.2f}"
            )
            return [best_step1_market_address, best_step2_market_address]

        self.logger.error(f"No two-hop swap route found for tokens: {in_token_address} -> {out_token_address}")
        return None

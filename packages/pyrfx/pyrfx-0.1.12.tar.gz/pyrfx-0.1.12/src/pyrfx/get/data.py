import logging
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any

from eth_typing import ChecksumAddress
from web3.contract import Contract

from pyrfx.config_manager import ConfigManager
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import get_reader_contract, save_csv, save_json, timestamp_df


class Data(ABC):
    """
    A base class responsible for handling data retrieval and processing for various markets.
    Provides support for retrieving token prices, processing market information, and saving data in JSON or CSV formats.
    """

    markets: Markets | None = None

    @abstractmethod
    def __init__(
        self,
        config: ConfigManager,
        use_local_datastore: bool = False,
        filter_swap_markets: bool = True,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize the GetData object for data processing.

        :param config: ConfigManager object containing chain-specific configuration.
        :param use_local_datastore: Whether to use local datastore for processing.
        :param filter_swap_markets: Boolean to filter out swap markets during processing.
        :param log_level: Logging level for this class.
        """
        self.config: ConfigManager = config
        self.use_local_datastore: bool = use_local_datastore
        self.filter_swap_markets: bool = filter_swap_markets

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self._prices: dict[str, dict[str, Any]] | None = None

        if Data.markets is None and self.config:
            Data.markets = Markets(self.config)

        self.reader_contract: Contract = get_reader_contract(config)
        self.output: dict[str, dict | str] = {"long": {}, "short": {}, "parameter": ""}

    def get_data(self) -> dict[str, Any]:
        """
        Retrieve and process market data, with optional outputs in JSON or CSV formats.

        :return: Processed data in dictionary format.
        """
        try:
            if self.filter_swap_markets:
                self._filter_swap_markets()

            data: dict = self._get_data_processing()

            # Optionally save the data to JSON or CSV
            if self.config.save_to_json:
                self._save_to_json(data)

            if self.config.save_to_csv:
                self._save_to_csv(data)

            return data
        except Exception as e:
            self.logger.error(f"Failed to retrieve data: {e}")
            raise

    def _get_data_processing(self) -> dict[str, Any]:
        """
        Perform data processing. To be overridden by subclasses with specific data processing logic.

        :return: Processed data dictionary.
        """
        raise NotImplementedError("Subclasses should implement their data processing logic here.")

    def _save_to_json(self, data: dict[str, Any]) -> None:
        """
        Save data to a JSON file in the datastore.

        :param data: Data to save as JSON.
        """
        file_name: str = f"{self.config.chain}_{data['parameter']}_data.json"
        save_json(
            output_data_path=self.config.data_path,
            file_name=file_name,
            data=data,
        )
        self.logger.info(f"Data saved as JSON: {file_name}")

    def _save_to_csv(self, data: dict[str, Any]) -> None:
        """
        Save data to CSV files in the datastore, handling both long and short data.

        :param data: Data to save as CSV.
        """
        try:
            for key in ["long", "short"]:
                if key in data:
                    file_name: str = f"{self.config.chain}_{key}_{data['parameter']}_data.csv"
                    save_csv(
                        output_data_path=self.config.data_path,
                        file_name=file_name,
                        data=timestamp_df(data[key]),
                    )
                    self.logger.info(f"Data saved as CSV: {file_name}")
        except KeyError as e:
            self.logger.error(f"KeyError while saving CSV: {e}")
        except Exception as e:
            self.logger.error(f"Error saving CSV: {e}")

    def _get_token_addresses(self, market_address: ChecksumAddress) -> tuple[ChecksumAddress, ChecksumAddress]:
        """
        Get the long and short token addresses for a given market.

        :param market_address: The address of the market to retrieve token addresses.
        """
        try:
            long_token_address = Data.markets.get_long_token_address(market_address=market_address)
            short_token_address = Data.markets.get_short_token_address(market_address=market_address)
            self.logger.info(f"Long Token: {long_token_address}, Short Token: {short_token_address}")
            return long_token_address, short_token_address
        except KeyError as e:
            self.logger.error(f"Error retrieving token addresses for market {market_address}: {e}")

    def _filter_swap_markets(self) -> None:
        """
        Filter out swap markets from the markets data.
        """
        markets_to_remove: list[ChecksumAddress] = [
            market_address
            for market_address in Data.markets.data
            if "SWAP" in Data.markets.get_market_symbol(market_address=market_address)
        ]
        for address in markets_to_remove:
            Data.markets.data.pop(address, None)
        self.logger.debug(f"Filtered {len(markets_to_remove)} swap markets.")

    def _get_pnl(
        self, market: list[str], prices_list: list[int], is_long: bool, maximize: bool = False
    ) -> tuple[Any, Any]:
        """
        Retrieve the Profit and Loss (PnL) and Open Interest with PnL for a market.

        :param market: List of market parameters.
        :param prices_list: List of prices corresponding to the market tokens.
        :param is_long: Boolean indicating if the position is long.
        :param maximize: Boolean indicating whether to maximize the PnL.
        :return: Tuple containing Open Interest with PnL and PnL.
        """
        try:
            open_interest_pnl = self.reader_contract.functions.getOpenInterestWithPnl(
                self.config.contracts.data_store.contract_address, market, prices_list, is_long, maximize
            )

            pnl = self.reader_contract.functions.getPnl(
                self.config.contracts.data_store.contract_address, market, prices_list, is_long, maximize
            )

            return open_interest_pnl, pnl
        except Exception as e:
            self.logger.error(f"Error getting PnL for market {market}: {e}")
            return None, None

    def _get_oracle_prices(
        self,
        market_address: ChecksumAddress,
        index_token_address: ChecksumAddress,
        long_token_address: ChecksumAddress,
        short_token_address: ChecksumAddress,
        return_tuple: bool = False,
    ) -> tuple[tuple[int, int], ...] | Any:
        """
        Get the oracle prices for a given market from the reader contract.

        :param market_address: The address of the market.
        :param index_token_address: The address of the index token.
        :param long_token_address: The address of the long token.
        :param short_token_address: The address of the short token.
        :param return_tuple: Boolean to return prices as a tuple.
        :return: Reader contract call or a tuple of prices.
        """
        if not self._prices:
            self._prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

        try:
            processed_prices = (
                (
                    int(self._prices[index_token_address]["minPriceFull"]),
                    int(self._prices[index_token_address]["maxPriceFull"]),
                ),
                (
                    int(self._prices[long_token_address]["minPriceFull"]),
                    int(self._prices[long_token_address]["maxPriceFull"]),
                ),
                (
                    int(self._prices[short_token_address]["minPriceFull"]),
                    int(self._prices[short_token_address]["maxPriceFull"]),
                ),
            )
        except KeyError as e:
            self.logger.warning(f"KeyError: Missing price information for market key {market_address}: {e}")
            return None

        if return_tuple:
            return processed_prices

        try:
            return self.reader_contract.functions.getMarketInfo(
                self.config.contracts.data_store.contract_address, processed_prices, market_address
            )
        except Exception as e:
            self.logger.error(f"Error retrieving market info for {market_address}: {e}")
            return None

    @staticmethod
    def _format_market_info_output(output: Any) -> dict[str, Any]:
        """
        Format the raw market info output into a structured dictionary.

        :param output: Raw market info data from the reader contract.
        :return: Formatted market info dictionary.
        """
        return {
            "market_address": output[0][0],
            "index_address": output[0][1],
            "long_address": output[0][2],
            "short_address": output[0][3],
            "borrowingFactorPerSecondForLongs": output[1],
            "borrowingFactorPerSecondForShorts": output[2],
            "baseFunding_long_fundingFeeAmountPerSize_longToken": output[3][0][0][0],
            "baseFundinglong_fundingFeeAmountPerSize_shortToken": output[3][0][0][1],
            "baseFundingshort_fundingFeeAmountPerSize_longToken": output[3][0][1][0],
            "baseFundingshort_fundingFeeAmountPerSize_shortToken": output[3][0][1][1],
            "baseFundinglong_claimableFundingAmountPerSize_longToken": output[3][1][0][0],
            "baseFundinglong_claimableFundingAmountPerSize_shortToken": output[3][1][0][1],
            "baseFundingshort_claimableFundingAmountPerSize_longToken": output[3][1][1][0],
            "baseFundingshort_claimableFundingAmountPerSize_shortToken": output[3][1][1][1],
            "longsPayShorts": output[4][0],
            "fundingFactorPerSecond": output[4][1],
            "nextSavedFundingFactorPerSecond": output[4][2],
            "nextFunding_long_fundingFeeAmountPerSize_longToken": output[4][3][0][0],
            "nextFunding_long_fundingFeeAmountPerSize_shortToken": output[4][3][0][1],
            "nextFunding_baseFundingshort_fundingFeeAmountPerSize_longToken": output[4][3][1][0],
            "nextFunding_baseFundingshort_fundingFeeAmountPerSize_shortToken": output[4][3][1][1],
            "nextFunding_baseFundinglong_claimableFundingAmountPerSize_longToken": output[4][4][0][0],
            "nextFunding_baseFundinglong_claimableFundingAmountPerSize_shortToken": output[4][4][0][1],
            "nextFunding_baseFundingshort_claimableFundingAmountPerSize_longToken": output[4][4][1][0],
            "nextFunding_baseFundingshort_claimableFundingAmountPerSize_shortToken": output[4][4][1][1],
            "virtualPoolAmountForLongToken": output[5][0],
            "virtualPoolAmountForShortToken": output[5][1],
            "virtualInventoryForPositions": output[5][2],
            "isDisabled": output[6],
        }

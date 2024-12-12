# ⚠️ Warning: Beta Version ⚠️

This SDK is currently in beta version and actively under development. It may contain bugs, incomplete features, and breaking changes. Use with caution. Feedback and contributions are welcome to help improve its stability and functionality.

# Limitations
- zkSync Sepolia testnet was deprecated and is not functional. 

# RFX Python SDK

A Python-based SDK developed for interacting with RFX Exchange, offering tools and scripts for executing various operations, including trading and liquidity management.

## Table of Contents
- [Usage](#usage)
- [Local Installation](#local-installation)
- [Local Build](#local-build)
- [Running Tests](#running-tests)
- [Building Documentation](#building-documentation)
- [DOC: GET Classes](#get-classes)
- [DOC: Order Classes](#order-classes)
- [DOC: Utils](#utils)


## Usage
The SDK can be installed via pip:
```sh
pip install pyrfx
```

## Local Installation
The supported Python versions: >= 3.10 <4

To set up the project locally, follow these steps:
1) Install packages: 
```sh
  poetry install --with dev  
```
2) If you are actively developing your project and need changes to the source code (src/pyrfx) to be immediately reflected without reinstalling the package every time, you can additionally use the editable install. This step allows you to make modifications in your code and see them reflected immediately.
```sh
  poetry run pip install -e .  
```

## Local build
```sh
mkdir dist/
cd ./dist
poetry build
```

## Running Tests
To execute tests:
```sh
poetry run pytest
```

## Building Documentation
To build HTML documentation:
```sh
poetry run pdoc src/pyrfx examples -o docs
```


## GET Classes

### AvailableLiquidity Class

The `AvailableLiquidity` class, inheriting from `Data`, is used to calculate and log available liquidity for long and short positions across multiple markets.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for chain-specific configurations, an optional flag (`use_local_datastore`) to specify local datastore usage, and a logging level (`log_level`).
- **Logging**: Uses a logger to provide detailed information on the liquidity computation process.
- **Data Processing**: Implements `_get_data_processing()` to process available liquidity for each market using Web3 contract calls and price data from Oracle.
- **Precision Calculation**: Uses `_get_precision_factors()` to calculate precision factors for long, short, and oracle prices.
- **Token Price Fetching**: The `_get_token_price()` method fetches the recent token prices with error handling.
- **Liquidity Calculation**: The `_log_liquidity()` method calculates and logs the available liquidity for long and short positions, providing insight into the market state.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
available_liquidity: dict = AvailableLiquidity(config=config).get_data()
```

### BorrowAPR Class

The `BorrowAPR` class, inheriting from `Data`, is used to retrieve and calculate the Borrow Annual Percentage Rate (APR) for long and short positions across multiple blockchain markets.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for chain-specific configurations and a logging level (`log_level`).
- **Logging**: Uses a logger to provide detailed information during APR data computation.
- **Data Processing**: Implements `_get_data_processing()` to generate and calculate long and short borrow APR for each market, utilizing parallel data processing for efficiency.
- **Threaded Processing**: The class uses `execute_threading()` to handle data retrieval concurrently, improving performance for large datasets.
- **APR Calculation**: The `_process_threaded_output()` method calculates and logs borrow APR values for long and short positions based on the threaded data.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
borrow_apr: dict = BorrowAPR(config=config).get_data()
```

### ClaimableFees Class

The `ClaimableFees` class, inheriting from `Data`, retrieves and calculates the total claimable fees (both long and short) across blockchain markets.

#### Key Features
- **Initialization**: Takes a `ConfigManager` object to handle chain configurations, and a logging level (`log_level`).
- **Logging**: Uses a logger to log detailed information during the fee calculation process.
- **Data Processing**: Implements `_get_data_processing()` to compute the total claimable fees for each market in USD.
- **Threaded Processing**: Uses `execute_threading()` to retrieve data in parallel for long and short claimable fees, boosting performance.
- **Oracle Price Fetching**: Fetches prices via the `OraclePrices` class for accurate USD valuation of fees.
- **Claimable Fee Calculation**: The `_calculate_total_fees()` method computes the total fees and logs the result, converting raw outputs into USD values.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
claimable_fees: dict = ClaimableFees(config=config).get_data()
```

### ContractBalance Class

The `ContractBalance` class, inheriting from `Data`, retrieves the USD balance of contracts in liquidity pools across multiple blockchain markets. It integrates smoothly into the SDK and supports blockchain data retrieval for pool liquidity analysis.

#### Key Features
- **Initialization**: Takes a `ConfigManager` object for chain-specific configurations and a logging level (`log_level`).
- **Logging**: Uses a logger to log information about the pool balances during the data fetching and computation processes.
- **Oracle Price Integration**: Fetches oracle prices via the `OraclePrices` class for calculating the USD equivalent of token balances.
- **Pool Balance Calculation**: Implements `get_pool_balances()` to query token balances from available markets and compute the total value in liquidity pools.
- **Saving Data**: Optionally saves the pool balance data to a JSON file if the `ConfigManager` has `save_to_json` enabled.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
contract_balances: dict = ContractBalance(config=config).get_pool_balances()
```

### Data Base Class

The `Data` class serves as an abstract base class for retrieving and processing blockchain market data. It provides a foundation for handling token prices, managing market information, and saving data in various formats.

#### Key Features
- **Initialization**: Takes a `ConfigManager` object for chain-specific configurations and a logging level (`log_level`). Supports optional use of a local datastore and filtering of swap markets.
- **Logging**: Uses a logger to provide detailed logs during data processing.
- **Market Information Handling**: Includes methods to retrieve long and short token addresses for each market, as well as filtering out swap markets.
- **Data Saving**: Supports saving data in both JSON (`_save_to_json()`) and CSV (`_save_to_csv()`) formats, allowing for easy data export.
- **Oracle Prices Integration**: Fetches prices from `OraclePrices` to facilitate calculations.
- **PnL Calculation**: Includes a method (`_get_pnl()`) to retrieve the Profit and Loss (PnL) and Open Interest with PnL for a market.
- **Market Information Retrieval**: `_get_oracle_prices()` and `_get_token_addresses()` are used for gathering token price information from the reader contract and managing the data associated with markets.
- **Abstract Data Processing**: Defines an abstract `_get_data_processing()` method, intended to be implemented by subclasses for specific data processing logic.

#### Example Usage
As this is an abstract base class, you would use it by extending it in a subclass. Here is a simple example of how to do that:

### EstimateSwapOutput Class

The `EstimateSwapOutput` class is used to estimate the swap output between two tokens on a blockchain network. It utilizes market data, available liquidity, and oracle price information to provide an estimate of the output token amount and price impact.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for chain-specific configurations and a dictionary of markets. The logging level (`log_level`) can also be specified.
- **Logging**: Uses a logger to provide detailed information about the token swap process.
- **Swap Output Estimation**: Implements `get_swap_output()` to estimate the amount of output tokens for a given input token and amount, including resolving token addresses and calculating price impacts.
- **Swap Route Determination**: Utilizes `SwapRouter` to determine the optimal swap route based on the available markets.
- **Market Price Integration**: Fetches recent prices using the `OraclePrices` class to accurately calculate the swap output in USD.
- **Support for Multiple Tokens**: Can handle multiple tokens and dynamically resolves token addresses if not provided.

#### Example Usage
```sh
# Initialize parameters
parameters: dict[str, str | float] = {
    "start_token_symbol": "WETH",
    "out_token_symbol": "USDC",
    "token_amount": 0.4,
}
config: ConfigManager = ConfigManager(...)
available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(config=config).get_available_markets()
eso: EstimateSwapOutput = EstimateSwapOutput(config=config, markets=available_markets)
swap_output: dict[str, float] = eso.get_swap_output(
    start_token_symbol=parameters["start_token_symbol"],
    out_token_symbol=parameters["out_token_symbol"],
    token_amount=parameters["token_amount"],
)
```

### FundingAPR Class

The `FundingAPR` class is responsible for calculating funding APRs for long and short positions in RFX blockchain markets. It can retrieve data from a local datastore or directly from an API, perform multithreaded calculations, and log results.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for blockchain configurations, an optional flag (`use_local_datastore`) for data retrieval, and a logging level (`log_level`).
- **Data Loading**: Loads open interest data either from a local JSON file or from an API (`_load_open_interest_data()`).
- **Data Processing**: The `_get_data_processing()` method retrieves relevant market data, processes it in a multithreaded manner, and calculates funding APR.
- **Market Information Handling**: Gathers token addresses and oracle prices for each market (`_process_market_key()`).
- **Funding Fee Calculation**: Uses the `_process_threaded_output()` method to calculate funding APR fees for long and short positions based on oracle prices and interest values.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
funding_apr: dict = FundingAPR(config=config).get_data()
```

### Markets Class

The `Markets` class is responsible for retrieving and managing blockchain market data, including token addresses and metadata for different markets. It provides methods for accessing market-specific information and integrates seamlessly with the overall SDK.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for blockchain configurations, and a logging level (`log_level`).
- **Market Data Retrieval**: Retrieves and processes raw market data using a reader contract, organizing it into a structured dictionary (`_process_markets()`).
- **Token Address Access**: Provides methods to access long, short, and index token addresses for each market (`get_long_token_address()`, `get_short_token_address()`, `get_index_token_address()`).
- **Market Metadata**: Retrieves additional market-specific metadata, such as the market symbol, decimal factors, and whether a market is synthetic.
- **Market Filtering**: Filters out markets that are not in the signed prices API to ensure only live, valid markets are processed.
- **Swap Market Handling**: Handles both standard and swap markets, with logic to generate appropriate market symbols and metadata.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
available_markets: dict = Markets(config=config).get_available_markets()
```

### OpenInterest Class

The `OpenInterest` class retrieves and processes open interest data for long and short positions across RFX blockchain markets. It uses oracle price data and multi-threaded calculations to provide efficient and accurate data analysis.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for blockchain configurations and a logging level (`log_level`).
- **Open Interest Calculation**: Uses the `_get_data_processing()` method to calculate open interest by fetching market data and using multi-threaded execution for efficiency.
- **Oracle Price Integration**: Retrieves oracle prices using the `OraclePrices` class to determine market pricing information.
- **Multi-threading Execution**: The `_execute_multithreading()` method is used to process multiple calculations concurrently, improving performance.
- **Precision Handling**: Determines precision factors for synthetic and non-synthetic markets (`_get_precision_factor()`) to accurately calculate open interest values.
- **Logging Results**: Logs the final calculated values for long and short open interest, providing a clear summary of the market data.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
open_interest: dict = OpenInterest(config=config).get_data()
```

### OpenPositions Class

The `OpenPositions` class is responsible for retrieving and processing open positions for a given blockchain address. It fetches open positions from a reader contract and processes them into a structured format, including detailed metrics like leverage and profit percentage.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for chain-specific configurations, an optional address for querying, and a logging level (`log_level`).
- **Open Position Retrieval**: Uses the `get_open_positions()` method to fetch and process all open positions for the given address.
- **Market Data Integration**: Integrates with available market data to provide context and symbols for each open position.
- **Leverage and Price Calculation**: Calculates key metrics for each open position, including entry price, leverage, mark price, and profit percentage (`_calculate_position_metrics()`).
- **Oracle Price Integration**: Uses the `OraclePrices` class to retrieve recent oracle prices for calculating the mark price of a position.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
open_positions: dict = OpenPositions(config=config).get_open_positions()
```

### OraclePrices Class

The `OraclePrices` class is responsible for fetching and processing the latest signed token prices from the RFX API for various blockchain networks. It integrates with the `ConfigManager` to configure the relevant API endpoint based on the blockchain network.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for blockchain configurations and a logging level (`log_level`).
- **Price Retrieval**: Uses the `get_recent_prices()` method to make a GET request to the RFX Oracle API and retrieve signed token prices.
- **Request Handling**: Implements error handling for request failures (`_make_query()`) and validates the response format (`_process_output()`).
- **Logging**: Logs the progress of requests and the processing of token prices.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
prices: dict = OraclePrices(config=config).get_recent_prices()
```

### PoolTVL Class

The `PoolTVL` class retrieves and calculates the Total Value Locked (TVL) in USD across all pools for a given blockchain. It uses data from oracle prices and a data store contract to determine the value of tokens in each pool.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for chain-specific configurations and a logging level (`log_level`). Also initializes oracle price data and data store contract.
- **TVL Calculation**: The `get_pool_balances()` method calculates the TVL for each pool by querying token balances and calculating their equivalent USD values.
- **Oracle Price Integration**: Uses the `OraclePrices` class to fetch the most recent prices of tokens, which are then used to calculate USD values.
- **Data Store Contract Integration**: Uses a Web3 contract to query the current token balances for both long and short positions in each pool.
- **Logging and Data Saving**: Logs detailed TVL information for each market and saves the TVL data to JSON and/or CSV formats, if configured to do so.

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
pool_tvl_data: dict = PoolTVL(config=config).get_pool_balances()
```

### RPPrices Class

The `RPPrices` class is responsible for calculating Reward Pool (RP) prices for various market actions, such as withdrawal, deposit, and trading, in the blockchain ecosystem. It extends the `Data` class to use common market and token retrieval functionalities and processes market prices using contract queries.

#### Key Features
- **Initialization**: Accepts a `ConfigManager` object for chain-specific configurations, a logging level (`log_level`), and initializes a reader contract to interact with the blockchain.
- **Market Actions**: Provides methods to calculate RP prices for different actions:
  - `get_price_withdraw()`: Fetches RP prices for withdrawing from a liquidity pool.
  - `get_price_deposit()`: Fetches RP prices for depositing into a liquidity pool.
  - `get_price_traders()`: Fetches RP prices for traders.
- **Multithreading**: Implements threading for price calculations to improve performance when querying multiple markets concurrently.
- **Market Data Preparation**: Uses `_prepare_market_data()` to gather the relevant market addresses and token information needed for price queries.
- **Data Processing**: Uses `_process_output()` to convert the raw outputs into a more structured and human-readable format.
- **Data Saving**: Saves the processed RP prices to JSON or CSV formats if configured (`_save_output()`).

#### Example Usage
```sh
config: ConfigManager = ConfigManager(...)
rp_prices: dict = RPPrices(config=config).get_price_traders()
```

## Order Classes

### DecreaseOrder Class
The DecreaseOrder class is used to manage and execute decrease orders (sell or close positions) on the RFX Exchange.

#### Key Features
- **Initialization:** Configures parameters such as market address, collateral, position size, slippage, and optional swap paths.
- **Gas Limit Handling:** Determines appropriate gas limits using the datastore contract.
- **Order Execution:** Builds and submits a decrease order with execution fees, acceptable prices, and price impact checks.
- **Integration:** Utilizes market and oracle price data for accurate calculations.

#### Example Usage
```sh
order = DecreaseOrder(
    config=config,
    market_address=market_address,
    collateral_address=collateral_address,
    index_token_address=index_token_address,
    is_long=False,
    size_delta=100,
    initial_collateral_delta=50,
    slippage_percent=0.05,
    debug_mode=True,
)
order.create_and_execute()
```

### IncreaseOrder Class
The IncreaseOrder class is used to manage and execute increase orders (buy or open positions) on the RFX Exchange.

#### Key Features
- **Initialization:** Configures parameters such as market address, collateral, position size, slippage, and optional swap paths.
- **Gas Limit Handling:** Determines appropriate gas limits using the datastore contract.
- **Order Execution:** Builds and submits an increase order with execution fees, acceptable prices, and price impact checks.
- **Integration:** Utilizes market and oracle price data for accurate calculations.

#### Example Usage
```sh
order = IncreaseOrder(
    config=config,
    market_address=market_address,
    collateral_address=collateral_address,
    index_token_address=index_token_address,
    is_long=True,
    size_delta=100,
    initial_collateral_delta=50,
    slippage_percent=0.05,
    debug_mode=True,
)
order.create_and_execute()
```

### DepositOrder Class
The DepositOrder class is used to manage and execute deposit orders in the RFX Exchange.

#### Key Features
- **Initialization:** Configures parameters such as market address, token addresses, and amounts for both long and short deposits.
- **Gas Limit Handling:** Determines appropriate gas limits using the datastore contract for deposit operations.
- **Integration:** Extends the base Deposit class to handle deposit-specific logic and operations.

#### Example Usage
```sh
order = DepositOrder(
    config=config,
    market_address=market_address,
    initial_long_token_address=long_token_address,
    initial_short_token_address=short_token_address,
    long_token_amount=1000,
    short_token_amount=500,
    debug_mode=True,
)
order.create_and_execute()
```


### WithdrawOrder Class
The WithdrawOrder class is used to create and manage withdrawal orders in the RFX Exchange.

#### Key Features
- **Initialization:** Configures parameters such as market address, token address for withdrawal, and the amount of RP tokens to withdraw.
- **Gas Limit Handling:** Determines appropriate gas limits using the datastore contract for withdrawal operations.
- **Integration:** Extends the base Withdraw class to handle withdrawal-specific logic and operations.

#### Example Usage
```sh
order = WithdrawOrder(
    config=config,
    market_address=market_address,
    out_token=out_token_address,
    rp_amount=1000,
    debug_mode=True,
)
order.create_and_execute()
```

### SwapOrder Class
The SwapOrder class is used to create and manage token swap orders in the RFX Exchange.

#### Key Features
- **Initialization:** Configures parameters such as token addresses, market details, swap path, slippage, and optional execution fees.
- **Gas Limit Handling:** Determines appropriate gas limits for single or multiple swap operations using the datastore contract.
- **Swap Estimation:** Includes functionality to estimate swap output and price impact based on token amounts and market data.
- **Integration:** Extends the base Order class to handle swap-specific logic and operations.

#### Example Usage
```sh
order = SwapOrder(
    config=config,
    start_token_address=start_token,
    out_token_address=out_token,
    market_address=market_address,
    collateral_address=collateral_address,
    index_token_address=index_token_address,
    initial_collateral_delta=1000,
    slippage_percent=0.01,
    swap_path=[start_token, out_token],
    debug_mode=True,
)
order.create_and_execute()
```

## Utils

### ConfigManager Class
The ConfigManager class manages blockchain configuration settings, including RPC URLs, wallet addresses, chain information, and contract details.

#### Key Features
- **Initialization:** Sets up network configurations, user wallet details, and data storage options for a specified blockchain network.
- **Contract Management:** Loads contract addresses and ABIs for network-specific contracts.
- **Checksum Conversion:** Converts Ethereum addresses to checksum format for accuracy and compatibility.
- **Environment Integration:** Supports fetching wallet addresses and private keys from environment variables.
- **Data Saving Options:** Provides flags to enable saving output data to JSON or CSV formats.

#### Example Usage
```sh
config = ConfigManager(
    chain="zkSync",
    user_wallet_address="0xYourWalletAddress",
    private_key="YourPrivateKey",
    save_to_json=True,
    output_data_folder="./data",
)
print(config)
```

### CustomErrorParser Class
The CustomErrorParser class is designed to parse Solidity errors returned from blockchain transactions. It supports decoding errors based on ABI definitions, Panic codes, and standard error strings.

#### Key Features
- **ABI-Based Error Parsing:** Matches error bytes against the ABI to identify custom errors and decode parameters.
- **Panic Code Decoding:** Parses Solidity Panic(uint256) errors and maps panic codes to descriptive messages.
- **Standard Error Parsing:** Decodes Solidity Error(string) messages.
- **Fallback Parsing:** Attempts to parse errors as generic strings when standard parsing fails.

#### Example Usage
```sh
parser = CustomErrorParser(config=config)
error_bytes = "0x12345678abcdef"  # Replace with actual error bytes
parsed_error = parser.parse_error(error_bytes)
print(parsed_error)
```

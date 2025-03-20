 // SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.7;

// ----------------------INTERFACE------------------------------

// Aave Interface
interface ILendingPool {
    function liquidationCall(
        address collateralAsset,
        address debtAsset,
        address user,
        uint256 debtToCover,
        bool receiveAToken
    ) external;

    function getUserAccountData(address user)
        external
        view
        returns (
            uint256 totalCollateralETH,
            uint256 totalDebtETH,
            uint256 availableBorrowsETH,
            uint256 currentLiquidationThreshold,
            uint256 ltv,
            uint256 healthFactor
        );
}

// ERC-20 Interface
interface IERC20 {
    function balanceOf(address owner) external view returns (uint256);
    function approve(address spender, uint256 value) external;
    function transfer(address to, uint256 value) external returns (bool);
}

// WETH Interface
interface IWETH is IERC20 {
    function withdraw(uint256) external;
}

// UniswapV2 Interfaces
interface IUniswapV2Callee {
    function uniswapV2Call(
        address sender,
        uint256 amount0,
        uint256 amount1,
        bytes calldata data
    ) external;
}

interface IUniswapV2Factory {
    function getPair(address tokenA, address tokenB)
        external
        view
        returns (address pair);
}

interface IUniswapV2Pair {
    function swap(
        uint256 amount0Out,
        uint256 amount1Out,
        address to,
        bytes calldata data
    ) external;
    function getReserves()
        external
        view
        returns (
            uint112 reserve0,
            uint112 reserve1,
            uint32 blockTimestampLast
        );
}

// ----------------------IMPLEMENTATION------------------------------
contract LiquidationOperator is IUniswapV2Callee {
    uint8 public constant health_factor_decimals = 18;

    // Constants for tokens, Uniswap pairs, and Aave lending pools
    address constant WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2; // WETH
    address constant USDT = 0xdAC17F958D2ee523a2206206994597C13D831ec7; // USDT
    address constant WBTC = 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599; // WBTC
    address constant AAVE_LENDING_POOL = 0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9; // Aave v2 Lending Pool
    address constant UNISWAP_FACTORY = 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f; // UniswapV2 Factory
    address constant TARGET_USER = 0x59CE4a2AC5bC3f5F225439B2993b86B42f6d3e9F; // Target for liquidation

    ILendingPool lendingPool;
    IWETH weth;
    IERC20 usdt;

    constructor() {
        lendingPool = ILendingPool(AAVE_LENDING_POOL);
        weth = IWETH(WETH);
        usdt = IERC20(USDT);
    }

    // Receive function to handle ETH withdrawals from WETH
    receive() external payable {}

    // Main function for executing the liquidation
    function operate() external {
        // 1. Get user account data and ensure the user is liquidatable
        (
            ,
            ,
            ,
            ,
            ,
            uint256 healthFactor
        ) = lendingPool.getUserAccountData(TARGET_USER);

        require(healthFactor < 10**health_factor_decimals, "User is not liquidatable");

        // 2. Get the Uniswap pair for WETH and USDT
        address pair = IUniswapV2Factory(UNISWAP_FACTORY).getPair(WETH, USDT);
        require(pair != address(0), "Uniswap pair does not exist");

        // 3. Initiate a flash loan swap
        IUniswapV2Pair(pair).swap(0, 1000 * 1e6, address(this), abi.encode("flash loan")); // Example amount
    }

    // Callback function from UniswapV2
    function uniswapV2Call(
        address,
        uint256,
        uint256 amount1,
        bytes calldata
    ) external override {
        // Security check: ensure the call is from a legitimate Uniswap pair
        address pair = IUniswapV2Factory(UNISWAP_FACTORY).getPair(WETH, USDT);
        require(msg.sender == pair, "Unauthorized");

        // 1. Use the borrowed USDT to liquidate the target user on Aave
        usdt.approve(AAVE_LENDING_POOL, amount1);
        lendingPool.liquidationCall(WBTC, USDT, TARGET_USER, amount1, false);

        // 2. Convert WETH collateral to USDT to repay Uniswap
        uint256 wethBalance = weth.balanceOf(address(this));
        weth.withdraw(wethBalance);
        // Logic to swap WETH to USDT and repay Uniswap

        // 3. Repay Uniswap and keep any remaining profit
        // Example: Repay logic
        uint256 profit = address(this).balance - amount1;
        payable(msg.sender).transfer(profit);
    }
}
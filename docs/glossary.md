# Key Concepts in Perpetual Trading

## Order Book
The orderbook lists all buy and sell orders for a particular asset, organized by price and quantity. It shows the supply and demand in the market.

## Liquidity
Liquidity refers to the availability of assets for trading on an exchange or market. High liquidity means that assets can be traded quickly and with minimal price impact.

## Spread
The spread is the difference between the highest price a buyer is willing to pay (bid) and the lowest price a seller will accept (ask). A smaller spread indicates a lower price impact due to higher market efficiency.

## Open Interest
Open interest is the total number of outstanding contracts for a particular derivative contract. It is a measure of market depth and indicates the market activity level.

## Position Size
Position size refers to the total value of the asset that a trader holds in a particular trade. In leveraged trading, the position size is determined by the amount of collateral and the leverage applied. Position size is important because it influences both potential profits and risks.

## Collateral
Collateral is the asset traders must deposit to open and maintain a position in a perpetual contract. It serves as security to cover potential losses. The amount of required collateral depends on the leverage used and the position size. Sufficient collateral is crucial to avoid liquidation.

## Leverage
Leverage allows traders to amplify their position size by borrowing funds, enabling them to control larger positions with less capital. For example, with 10x leverage, a trader can open a 1 BTC position with just 6,400 USDC as collateral, even if the current BTC price is 64,000 USDC. While leverage increases potential profits, it also magnifies potential losses.

## Funding Rates
Funding rates are periodic payments exchanged between traders holding long and short positions in a perpetual contract. The purpose of funding rates is to keep the contract's price aligned with the spot price of the underlying asset. Depending on market conditions, either long or short-position holders may need to pay the other side.

The funding fee is calculated based on the difference between the index price and the mark price, as well as the interest rate for leverage trading.

## Mark Price
The Mark Price represents the best estimate of a perpetual futures contract’s value and is less volatile than the index or last price. It serves as the reference price for a perpetual contract and is used to prevent unnecessary liquidations caused by market manipulation.

## Index Price
The Index Price is the volume-weighted average of the underlying asset prices listed on major spot exchanges. It is used as a reference for pricing perpetual contracts.

## Last Price
The Last Price refers to the most recent traded price of the contract. It is often used to calculate PnL but is less reliable for preventing liquidation than the Mark Price.

## Liquidations
Liquidation occurs when a trader’s position is forcibly closed by the exchange due to insufficient collateral to cover potential losses. This typically happens when the market moves against the trader’s position, causing the collateral to fall below the required maintenance margin. Liquidations are essential for preventing further losses and protecting the exchange’s liquidity.

## Maintenance Margin
The maintenance margin is the minimum amount of collateral required to keep a position open. If a trader’s margin falls below this level, their position may be liquidated.

## Initial Margin
The initial margin is the amount of collateral needed to open a position. This requirement varies depending on the market and leverage used.

## Cross-Margin
Cross-margin is a margin system where the collateral across multiple positions in a trader’s account is pooled together. This approach reduces the risk of liquidation by allowing profits from one position to offset losses in another. However, it also increases overall risk, as significant losses in one position can impact the entire account.

## Auto De-leveraging (ADL) 
Auto de-leveraging is a mechanism that automatically liquidates positions when their margin falls below a certain level if other liquidation mechanisms fail. It is designed to protect the exchange from losses during extreme market conditions.

## Cost Position
The cost position is the average price at which a trader opens their position, including any associated costs like trading and funding fees. It is used to calculate unrealized PnL.

## Taker Fee
A taker fee is charged to traders who execute orders that immediately remove liquidity from the order book, typically through market orders.

## Maker Fee
A maker fee is charged to traders who place orders that add liquidity to the order book, typically through limit orders.

## Funding Fee 
References the funding rate, a periodic payment made between long and short traders to keep perpetual positions close to the market price of the underlying asset.

## Unrealized/Unsettled PnL
Unrealized PnL (Profit and Loss) refers to the potential profit or loss of an open trading position that has not yet been closed or settled. It represents the difference between the current market value of the asset and the entry price at which the position was opened.

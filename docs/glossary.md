# Key Concepts in Perpetual Trading

## Order Book
The orderbook lists all buy and sell orders for a particular asset, organized by price and quantity. It shows the supply and demand in the market. 

Orderly offers 60 different assets and has one specific orderbook for each listed market. 

## Liquidity
Liquidity refers to the availability of assets for trading on an exchange or market. High liquidity means that assets can be traded quickly and with minimal price impact.

## Spread
The spread is the difference between the highest price a buyer is willing to pay (bid) and the lowest price a seller will accept (ask). A smaller spread indicates a lower price impact due to higher market efficiency.

## Open Interest
Open interest is the total number of outstanding contracts for a particular derivative contract. It is a measure of market depth and indicates the market activity level.

## Position Mode
Orderly currently allows only one-sided mode: traders cannot hold both long and short positions for a single Perpetual Futures contract.

# Prices

## Index Price
It represents the "fair" or "spot" price of the underlying asset, typically derived from the asset's prices on several major spot exchanges. It is not the actual price of the perpetual contract itself but a way to prevent price manipulation and ensure that the contract price closely follows the real market value of the asset.
The index price serves as the reference price for funding rates. It ensures that traders are trading close to the true market value of the asset, preventing divergence from spot prices.

# Calculation
Orderly calculates it as a volume-weighted average of the underlying asset prices listed on major spot exchanges. To mitigate the risk of market manipulation, price deviation, and exchange connectivity issues. Orderly applies various protective measures to ensure a fair and accurate index price:

- If for 1 single source, the price deviates by more than 5% from the median price of all sources, Orderly caps/floors the value at +/- 5%. Once the exchange-computed price falls below the 5% range, its original value will be taken.
- If multiple sources show a deviation of more than 5% from the median, Orderly will use the median instead of the volume-weighted average
- If there is a connectivity issue with a specific exchange that is not sending any price for a duration of 1min, its weight will be temporarily set to 0 in the calculation

In the Index Price calculation, the weights are computed every 5 minutes based on the 4-hour trading volume over the spot trading pairs of the selected centralized exchanges.

    Weight (CEX_i) = Volume (CEX_i) / Total Volume (CEXes)
    where:
        Volume (CEX_i) refers to the 4-hour trading vol of the CEX i
        Total Volume (CEXes) refers to the sum of the 4-hour trading volume accross all relevant CEXes for the specific pair

## Mark Price
The Mark Price represents the best estimate of a perpetual futures contract’s value and is less volatile than the index or last price. It serves as the reference price for a perpetual contract and is used to prevent unnecessary liquidations caused by market manipulation.

It is mainly used to calculate unrealized profit and loss (PnL) and determine liquidation, aiming to protect traders from being liquidated unfairly due to sudden market movements or manipulation.

### Calculation

To calculate it Orderly Network computes the Median Price of the three following components :

    Median Price = Median(P1, P2, Futures Price)
    where:
        P1 = Index Price * (1 + Last Funding Rate * Time until next Funding / dt)
        P2 = Index Price + 15 Minute Moving Average[Basis]
        Futures Price = Median(Bid0, Ask0, Last_Price)

    Last Funding Rate is expressed on a 8h basis

    Basis = Median(Bid0, Ask0) - Index Price, calculated as a snapshot every minute
    dt = Funding Period = 8 hours

Then Orderly applies a cap to the Mark Price relative to the Index Price defined by Factor (see table below) and Cap/Floor funding (cf Funding Rate section)

    Mark Price = Clamp(Median Price, Index Price * (1 + Factor * Cap Funding), Index Price * (1 + Factor * Floor_funding))
    cap_funding and floor_funding depend on the perpetual market (cf Funding Rate section)

## Summary of Key Differences between Mark and Index Prices:

| Aspect | Mark Price | Index Price |
| ------ | ---------- | ----------- |
| Definition | Smoothed price to avoid unfair liquidations | The fair market price of the asset, based on spot prices |
| Used For | Liquidations, calculating unrealized PnL | Calculating funding rates and as a reference for spot price |
| Volatility | Smoother to avoid unfair liquidations | Follows real-time market prices, more volatile |

In practice, the mark price is a protective measure, ensuring more stability for traders, while the index price reflects the broader market reality.

## Last Price
The Last Price refers to the latest transaction price at which a perpetual contract was traded in the orderbook. Said differently, the Last Price simply corresponds to the last trade in the trading history. It is used to calculate the realized PnL (see Margin, leverage & PnL section) and is less reliable for preventing liquidation than the Mark Price.

## Notional Value
Notional Value refers to the total value of the asset that a trader holds in a particular trade. On Orderly, the position size is determined by the number of perpetual contracts that the trader holds (Position Qty) and the asset’s Mark Price.  

    Notional Value = Position Qty * Mark Price
    Position Qty = Margin * Leverage / Mark Price

## Margin
Margin is the asset traders must deposit as collateral to open and maintain a position in a perpetual contract. It serves as security to cover potential losses. The amount of required collateral depends on the notional value and each specific market. Sufficient collateral is crucial to avoid liquidation.

## Single Collateral

Orderly offers USDC-based Perpetual Futures contracts, therefore the collateral is in USDC and all perpetual contracts are quoted and settled in USDC.
Cross-Margin

Finally, Orderly currently offers only cross-margin mode. As a trader, you can deposit USDC collateral and it will be shared across all open positions to calculate the margin ratio.

This allows profits from one trade to offset potential losses in another, reducing the likelihood of liquidation for individual positions. By sharing the margin across positions, traders can manage market volatility more effectively, but it also increases risk. If the overall account balance drops too low, all positions are at risk of liquidation, making it important for traders to monitor their overall portfolio carefully.

## Leverage
Since Orderly is built around leveraged trading, your collateral (margin) is only a portion of the notional value. The rest is borrowed using leverage, allowing traders to control large positions with a small amount of capital.

For example, with 10x leverage, a trader can open a 1 BTC position with just 6,400 USDC as collateral, even if the current BTC price is 64,000 USDC. While leverage increases potential profits, it also magnifies potential losses.

Orderly will enable the following leverages: 1x, 2x, 3x, 4x, 5x, 10x, and 20x.

## Margin Ratio
The margin ratio of an account is equal to the total collateral value divided by the total notional opened by the account (the total collateral value being the USDC balance plus any unrealized profit/loss).

The margin ratio defines the risk level of your account: a higher margin ratio leads to a lower risk level (with a default margin ratio set to 1000% meaning you have no open positions)

For an account having positions on i perpetual_markets:

    Margin_ratio = total_collateral_value / sum(abs(notional_value_i))  

## Initial Margin Ratio

To open a new futures position or execute withdrawals, the Margin Ratio of the Account has to be higher than the Initial Margin ratio. Otherwise, the account will not be able to open any new futures position or execute withdrawals.

Each Perpetual Futures market has a defined Initial Margin Ratio (Base IMR) and maximum leverage equal to 1/Base IMR.
    IMR i = Max(1 / Max Account Leverage, Base IMR i, IMR Factor i * Abs(Notional Value i)^(4/5))

IMR Factors are specific coefficients used to calculate the required margin for large positions. The larger the position, the lower the actual leverage that can be used. Factors can be found here.

## Maintenance Margin Ratio
An account will be liquidated if the Margin Ratio of the account is lower than the Maintenance Margin Ratio required. For more information go to Liquidations. 
    MMR i = Max(Base MMR i, Base MMR i / Base IMR i * IMR Factor i * Abs(Notional Value i)^(4/5))

## PnL
The unrealized PnL of an open position refers to the profits or losses of that position based on the Mark Price:

    Unrealized PnL(Perp Market i) = Position Qty * (Mark Price - Position Average Entry Price)

The realized PnL refers to the profits or losses after closing a position:

    Realized PnL(Perp Market i) = Position Qty * (Average Price - Position Average Entry Price)

## PnL Settling
On Orderly, settling PnL allows traders to move their profit or loss from all perpetual markets to their balance. PnL Settlement has no impact on the Account Margin Ratio or open positions.

It should be noted that settled/unsettled PnL and realized/unrealized PnL are different. PnL is realized when closing or reducing a position. The resulting realized PnL moves into the balance only when the trader triggers a PnL settlement.
Settled PnL into balance can be used for spot trading or withdrawn, but doing so will impact your margin ratio.

### The process of PnL Settlement is as follows:
When account X makes a call to settle PnL, Orderly will choose the top accounts with the largest unsettled opposing PnL. Starting from the largest account, each account’s unsettled PnL will be offset with account X, until account X has no more remaining PnL to settle.
As an Example: Account X has +20,000 USDC unsettled PnL with a balance of 100 USDC. The top 2 facing Accounts A and B have -15,000 USDC and -5,000 USDC unsettled PnL respectively:

First, settling Account X vs Account A will increase Account X’s balance by 15,000 USDC and decrease Account A’s balance by 15,000 USDC. Account X has a remaining unsettled PnL of +5,000 USDC and a balance of 15,100 USDC.
Then, settling Account X vs Account B will increase Account X’s balance by 5,000 USDC and decrease Account B’s balance by 5,000 USDC. Account X has a remaining unsettled PnL of 0 and a balance of 20,100 USDC. The settlement process ends since Account X has no remaining unsettled PnL.
Settling PnL will NOT change the user’s balance as the displayed user balance already includes unsettled PnL in the calculation. Withdrawable balance will change after settling PnL as it doesn’t include unsettled profits in the calculation.
All settling PnL does is move profits into the user’s account so the user can withdraw.

# Balance Formulas

## Account Margin Ratio
Current margin ratio = total_collateral_value / sum(abs(notional_value_i))

## Total Collateral
Total collateral of the user (doesn’t account for any pending orders, includes unsettled PnL) = total_balance + upnl + pending_short_USDC

## Free Collateral
Available collateral/balance to trade (accounts for any pending orders, includes unsettled PnL) = collateral + upnl - total_initial_margin_with_orders - pending_short_USDC

## Portfolio Value
Total potfolio value including position notionals = USDC Balance + (non USDC assets) * mid_price + unsettled pnl

## Withdrawable Balance
Collateral available to withdraw (excludes unsettled PnL) = total_balance - total_initial_margin_with_orders - positive_upnl

Examples
Ex. 1 user’s total_balance = 100 USDC, unsettled PnL = -40 USDC, => total_collateral is then 60 USDC. User has a position which takes up 20 USDC maintenance margin, then free_collateral or withdrawable_balance = 60 - 20 = 40 USDC
Ex. 2 user’s total_balance = 100 USDC, unsettled PnL = 40 USDC, => total_collateral is then 100 USDC. User has a position which takes up 20 USDC maintenance margin, then free_collateral = 100 - 20 = 80 USDC and withdrawable_balance = 80 - 40 = 40 USDC

## Funding Rate
The funding rate is a periodic cash flow exchanged between long and short position holders, ensuring the perpetual futures contract's price closely follows the underlying asset's price. On Orderly, it is expressed on an hourly basis and computed once every minute.
Premium Calculation

The funding rate is determined by the Premium, which measures the deviation between the contract price and the index price. To avoid funding manipulation, Orderly uses the Impact bid price and ask prices, rather than the highest bid and lowest ask only.
Impact Bid Price represents the average fill price to execute the Impact Margin Notional on the Bid Price.
Impact Ask Price represents the average fill price to execute the Impact Margin Notional on the Ask Price
Impact Margin Notional represents the notional available to open a position at maximum leverage based on the initial margin ratio of the perpetual market, given a specific amount of USDC as collateral.

The funding rate is then capped and floored with values that depend on the perpetual market.
accrued funding (dt) = Mark Price * Funding Rate (hourly) * dt
Premium (dt) = [Max(0, Impact Bid Price - Index Price) - Max(0, Index Price - Impact Ask Price)] / Index Price

dt : funding period    

## Funding Period
The Funding Rate is expressed on an hourly basis and will be computed once every minute (funding period is dt=60s). Every minute, a position on 1 perpetual contract will accrue:
accrued funding (dt) = Mark Price * Funding Rate (hourly) * dt
NB: dt is here expressed in hours (60/3600)

Once the Premium for a specific funding period has been computed, the funding rate as a function of the premium is a piecewise linear function with three main regions.
funding_rate = clamp [funding_function (Premium(dt)), cap_funding(perp_mkt), floor_funding(perp_mkt)]

- Low premiums : | x | < p1 ; slope1
- Medium premiums : p1 < | x | < p2 ; slope2
- Large premium : p2 < | x | < p3 ; slope3

| Premium | p_i | slope_i |
| ------- | --- | ------- |
| Low | `| x | < 0.5%` | 1/8 |
| Medium | `0.5% < | x | < 1.5%` | 1/4 |
| Large | `1.5% < | x |` |  1/2 |

p_i and slope_i values are subject to changes.

## Funding Settlement
The accrued funding of a position of an account is settled when there is a PnL settlement being called on that account (see PnL settlement)

## Liquidations
Liquidation occurs when a trader’s position is forcibly transferred by Orderly to liquidators due to insufficient collateral to cover potential losses. This typically happens when the market moves against the trader’s position, causing the collateral to fall below the required maintenance margin. Liquidations are essential for preventing further losses and protecting the exchange’s liquidity.

An account is subject to liquidation if its Account Margin Ratio falls below its Maintenance Margin Ratio. Orderly uses the Mark Price to represent a contract’s estimated value. As it derives from multiple reputable spot exchanges (see Index Price) and the funding rate, it is less volatile than the Last Price and discourages bad actors from manipulating the market price to trigger liquidations.
When an account is under liquidation, its current open orders are automatically canceled and its USDC balance is frozen.

## Decentralized Liquidations
Unlike Centralized Exchanges or a few other dApps such as dYdX, at Orderly, liquidations are decentralized.
Most of the time, CEXes directly close positions on the orderbook, which often triggers cascading liquidations, hurting traders further and encouraging bad actors to manipulate market prices.

Orderly adopts a decentralized liquidation model where positions are transferred to liquidators at a discount instead of being market sold in the orderbook. It is fully decentralized as anyone with an Orderly account can act as a liquidator, as long as the account has enough margin to take over the liquidated positions.

## Liquidation Trigger
A liquidation is triggered if the Account Margin Ratio (AMR) is below the Maintenance Margin Ratio (MMR) required for the account.

## Liquidation Tiers
All trading pairs are not equal in terms of risk. In Orderly, there are two groups of symbols:
Low Tier Risk = BTC & ETH, Liquidators can only claim a ratio of all symbols. Claiming a single symbol is not allowed
High Tier Risk = Others,  Liquidators can claim 1 single symbol

## Liquidation Amount
The amount of positions that need to be liquidated is calculated for both low tier and each symbol of high tier perp markets. Whenever possible, each amount is computed so that the Account Margin Ratio equals the Initial Margin Ratio.
If the account has multiple positions in the low tier risk, the positions will be partially liquidated in a volume-weighted fashion.

## Liquidation Fee

When an account is liquidated, a User Liquidation Fee is incurred. In Orderly, each market has its liquidation fee according to the table below.

| Perp Market | Liquidation Fee |
| ----------- | --------------- |
| BTC | 0.80% |
| ETH | 0.80% |
| Altcoins (10x) | 1.50% |
| Altcoins (20x) | 2.40% |


The overall User Liquidation Fee is calculated as follows:
Low Tier Liquidation (multiple symbols):

    User Liquidation Fee = Sum[Liquidation Fee(Symbol i) * Abs(Notional i)]

High Tier Liquidation (1 symbol):

    User Liquidation Fee = Liquidation Fee(Symbol i) * Abs(Notional i)


# Fees

## Cost Position 
The cost position is the average price at which a trader opens their position, including any associated costs like trading and funding fees. It is used to calculate unrealized PnL.

## Taker Fee
A taker fee is charged to traders who execute orders that immediately remove liquidity from the order book, typically through market orders.

## Maker Fee
A maker fee is charged to traders who place orders that add liquidity to the order book, typically through limit orders.

## Funding Fee 
References the funding rate, a periodic payment made between long and short traders to keep perpetual positions close to the market price of the underlying asset.

## Liquidation Fee
The incurred fee when an account is liquidated. For more details check Liquidations. 

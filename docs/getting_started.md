# Getting Started
> An overview of the steps required to get started


To begin using Orderly, you must first setup a wallet with some testnet ETH so you can begin making transactions.
For this example, we are going to assume you are using Arbitrum Sepolia.

!!! Asynchronous Python

    In this example, we use async python.  If you are in an [ipython](https://ipython.org){:target="_blank"} shell you can run these
    examples as is, but if you are working on a standard python file you will need to wrap these calls in an async
    function (ie. `async def amain()`), and then import asyncio and call `asyncio.run(amain())`

## Setting up your Orderly Account for SDK access

```python
from eth_rpc import *
from emp_orderly.onboarding import *

# create a new wallet
wallet = PrivateKeyWallet.create_new()
# print your private key so you can write it down for use later
print(wallet.address, wallet.private_key)

# create a new account on orderly
await create_account(wallet)

# create an orderly key from your wallet's private key
# NOTE: you can make as many orderly keys as you want, but this one is generated from your
#       wallets private key.  Keep this PRIVATE!
key_bytes = publickey(bytes.fromhex(wallet.private_key.removeprefix("0x")))
orderly_key = "ed25519:%s" % b58encode(key_bytes).decode("utf-8")

# register your new orderly key as a signer for your wallet address
await add_access_key(wallet, orderly_key)

# get some testnet USDC from the faucet
await faucet(wallet)

# deposit this testnet USDC to Orderly (NOTE: requires some ETH for gas)
await deposit(wallet)

# now you can initialize the SDK
sdk = EmpyrealOrderlySDK(pvt_hex=wallet.private_key, account_id=orderly_id, is_testnet=True)
```


## Making your First Trade

Lets open a long position on bitcoin and check its status to see how the SDK works

```python
from decimal import Decimal

from eth_rpc import *
from emp_orderly_types import *
from emp_orderly.onboarding import *

sdk = EmpyrealOrderlySDK(pvt_hex=wallet.private_key, account_id=orderly_id, is_testnet=True)


bitcoin_asset_info = await sdk.asset_info(PerpetualAssetType.BTC)
# this is the min tick size for an asset
base_min = Decimal(str(bitcoin_asset_info['data']['base_min']))
quote_tick = Decimal(str(bitcoin_asset_info['data']['quote_tick']))

bitcoin_market_info: MarketInfo = await sdk.get_market_info(PerpetualAssetType.BTC)

# the market info has information about the asset, such as its index price, mark price, vunding rates, volume, and more
bitcoin_price = bitcoin_market_info.index_price

# we want to buy $25, so let's divide 25 by the bitcoin price.  We're using the decimal module to keep precision in our
# decimal numbers
purchase_amount = (Decimal('25') / bitcoin_price).quantize(base_min)

# let's make the trade and open our position
response: OrderResponse = await sdk.make_order( purchase_amount, PerpetualAssetType.BTC, is_buy=True)
positions: PositionData = await sdk.positions()

# now we can see our current bitcoin position (assuming we have no other positions open)
print([position for position in positions.rows if position.symbol == PerpetualAssetType.BTC])
```

## Opening a Limit Order

Lets open a long position on bitcoin and check its status to see how the SDK works

```python
take_profit_price: Decimal = (bitcoin_price * Decimal('1.1')).quantize(quote_tick)
await sdk.make_limit_order('0.0005', price=take_profit_price, asset=PerpetualAssetType.BTC, is_buy=False)

# get all unfulfilled orders to see your open bitcoin order
orders: list[Order] = await sdk.orders(status="INCOMPLETE")
```

## Close Our Positions

Now we can close out our open orders and positions

```python
# now, let's close our open limit order
await sdk.close_orders(PerpetualAssetType.BTC)

# and we can close our bitcoin position
await sdk.close_position(PerpetualAssetType.BTC)
```

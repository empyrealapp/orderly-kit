# TL;DR
> A simplified version of the tutorial.

## Import and setup your SDK

```python
import os

from emp_orderly import (
    Strategy, EmpOrderly,
    crossover, plot_heatmaps,
    EMA, SMA, SLOPE, CHOP,
    EmpyrealOrderlySDK,
)
from emp_orderly_types import PerpetualAssetType, Interval, OrderType

pvt_hex = os.environ["PVT_KEY_HEX"]
sdk = EmpyrealOrderlySDK.register(pvt_hex)
```

### Deposit to your orderly account
Make sure to fund your wallet with USDC (or another valid deposit token)
```python
TBD
```

### Make a limit order
```python
# make limit order for bitcoin at $59000
await sdk.make_limit_order(amount=100, price=59_000, asset=PerpetualAssetType.BTC, is_buy=True)
```

### Make a Trade
```python
# short bitcoin for $100
await sdk.make_order(100, asset=PerpetualAssetType.BTC, is_buy=False)
```

### Close your Position
```python
# close all open postiions and orders
await sdk.close(PerpetualAssetType.BTC)
```

# Datafeeds
> Loading data for managing trading algorithms

```python
from emp_orderly.account import EmpyrealOrderlySDK
from emp_orderly_types import Interval, PerpetualAssetType

sdk = EmpyrealOrderlySDK(pvt_hex=wallet.private_key, account_id=orderly_id, is_testnet=True)

# returns a pandas dataframe
ohlcv_data = await sdk.get_ohlcv(PerpetualAssetType.BTC, resolution=Interval.hour, start_days_behind=3.0)

# Index(['open', 'high', 'low', 'close', 'volume_asset', 'volume'], dtype='object')
print(ohlcv_data.columns)

# get the MACD for the dataset
ohlcv_data.ta.macd()
```

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from .assets import PerpetualAssetType


class MarketInfo(BaseModel):
    symbol: PerpetualAssetType
    index_price: Decimal
    mark_price: Decimal
    sum_unitary_funding: Decimal
    est_funding_rate: Decimal
    last_funding_rate: Decimal
    next_funding_time: datetime
    open_interest: Decimal
    last_24h_open: Decimal = Field(alias="24h_open")
    last_24h_close: Decimal = Field(alias="24h_close")
    last_24h_high: Decimal = Field(alias="24h_high")
    last_24h_low: Decimal = Field(alias="24h_low")
    last_24h_volume: Decimal = Field(alias="24h_volume")
    last_24h_amount: Decimal = Field(alias="24h_amount")

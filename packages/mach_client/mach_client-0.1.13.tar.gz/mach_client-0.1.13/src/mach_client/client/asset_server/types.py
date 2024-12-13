from decimal import Decimal

from pydantic import BaseModel

from ..types import MachChain


class AssetPricingData(BaseModel):
    chain: MachChain
    address: str
    symbol: str
    decimals: int
    price: float
    daily_percent_change: float


class UserAssetData(BaseModel):
    chain: MachChain
    address: str
    balance: int
    symbol: str
    price: Decimal
    daily_percent_change: Decimal

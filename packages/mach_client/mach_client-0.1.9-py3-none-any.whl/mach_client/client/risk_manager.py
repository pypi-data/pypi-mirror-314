from abc import ABC, abstractmethod
import asyncio
import dataclasses
from decimal import Decimal
import typing
from typing import Optional

from ..asset import Token
from ..client.asset_server import AssetServer
from ..log import LogContextAdapter, Logger
from .types import Quote


@dataclasses.dataclass(kw_only=True)
class RiskAnalysis:
    reject: bool


class RiskManager(ABC):
    __slots__ = ("logger",)

    def __init__(self, logger: Logger):
        self.logger = logger

    @abstractmethod
    async def __call__(
        self, src_token: Token, dest_token: Token, quote: Quote
    ) -> RiskAnalysis:
        pass


class BaseSlippageManager(RiskManager):
    @dataclasses.dataclass(kw_only=True)
    class RiskAnalysis(RiskAnalysis):
        slippage: Optional[Decimal]
        slippage_tolerance: Decimal

    __slots__ = ("slippage_tolerance",)

    def __init__(
        self,
        slippage_tolerance: Decimal,
        logger: Logger,
    ):
        super().__init__(LogContextAdapter(logger, "Slippage Manager"))
        assert -1.0 <= slippage_tolerance <= 0.0
        self.slippage_tolerance = slippage_tolerance

    def will_check(self, src_token: Token, dest_token: Token) -> bool:
        return True

    async def get_value(self, token: Token, amount: int) -> Decimal:
        return token.to_coins(amount)

    @typing.override
    async def __call__(
        self, src_token: Token, dest_token: Token, quote: Quote
    ) -> RiskAnalysis:
        if not self.will_check(src_token, dest_token):
            self.logger.warning(f"Not checking {src_token} and {dest_token}")

            return self.RiskAnalysis(
                reject=False,
                slippage=None,
                slippage_tolerance=self.slippage_tolerance,
            )

        src_value, dest_value = await asyncio.gather(
            self.get_value(src_token, quote.src_amount),
            self.get_value(dest_token, quote.dst_amount),
        )

        slippage = dest_value / src_value - Decimal(1.0)
        self.logger.info(f"{src_token} => {dest_token} slippage: {100 * slippage}%")

        return self.RiskAnalysis(
            reject=slippage < self.slippage_tolerance,
            slippage=slippage,
            slippage_tolerance=self.slippage_tolerance,
        )


class SlippageManager(BaseSlippageManager):
    __slots__ = ("asset_server",)

    def __init__(
        self,
        asset_server: AssetServer,
        slippage_tolerance: Decimal,
        logger: Logger,
    ):
        super().__init__(slippage_tolerance, logger)
        self.asset_server = asset_server

    @typing.override
    def will_check(self, src_token: Token, dest_token: Token) -> bool:
        return self.asset_server.is_supported(
            src_token
        ) and self.asset_server.is_supported(dest_token)

    @typing.override
    async def get_value(self, token: Token, amount: int) -> Decimal:
        usd_price = await self.asset_server.get_price(token)
        return token.to_coins(amount) * usd_price


# Only checks "similar tokens". Doesn't need to make a network request.
class SimilarTokenSlippageManager(BaseSlippageManager):
    __slots__ = tuple()

    def __init__(self, slippage_tolerance: Decimal, logger: Logger):
        super().__init__(slippage_tolerance, logger)

    @typing.override
    def will_check(self, src_token: Token, dest_token: Token) -> bool:
        return (
            src_token.symbol == dest_token.symbol
            or (src_token.is_usd_stablecoin() and dest_token.is_usd_stablecoin())
            or (src_token.is_eth() and dest_token.is_eth())
            or (src_token.is_btc() and dest_token.is_btc())
            or (src_token.is_eur_stablecoin() and dest_token.is_eur_stablecoin())
            or (src_token.is_gbp_stablecoin() and dest_token.is_gbp_stablecoin())
            or (src_token.is_jpy_stablecoin() and dest_token.is_jpy_stablecoin())
            or (src_token.is_chf_stablecoin() and dest_token.is_chf_stablecoin())
        )

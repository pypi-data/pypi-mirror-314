import dataclasses
from datetime import timedelta
from typing import Any

from ..account import AccountID
from ..asset import Token
from ..transaction import SentTransaction, Transaction
from .risk_manager import RiskAnalysis
from .types import OrderResponse, Quote


@dataclasses.dataclass(frozen=True, slots=True)
class InsufficientSourceBalance:
    token: Token
    balance: int
    account_id: AccountID


@dataclasses.dataclass(frozen=True, slots=True)
class QuoteFailed:
    pair: tuple[Token, Token]
    amount: int
    account_id: AccountID
    exception: Exception


@dataclasses.dataclass(frozen=True, slots=True)
class QuoteLiquidityUnavailable:
    pair: tuple[Token, Token]
    amount: int
    account_id: AccountID
    quote: Quote


@dataclasses.dataclass(frozen=True, slots=True)
class OrderRejected:
    pair: tuple[Token, Token]
    amount: int
    account_id: AccountID
    quote: Quote


@dataclasses.dataclass(frozen=True, slots=True)
class RiskManagerRejection:
    pair: tuple[Token, Token]
    amount: int
    quote: Quote
    risk_analysis: RiskAnalysis


@dataclasses.dataclass(frozen=True, slots=True)
class SubmitOrderFailed:
    pair: tuple[Token, Token]
    amount: int
    place_order_transaction: SentTransaction
    exception: Exception


@dataclasses.dataclass(frozen=True, slots=True)
class SourceNotWithdrawn:
    pair: tuple[Token, Token]
    amount: int
    order: OrderResponse
    wait_time: timedelta


@dataclasses.dataclass(frozen=True, slots=True)
class DestinationNotReceived:
    pair: tuple[Token, Token]
    amount: int
    order: OrderResponse
    wait_time: timedelta


@dataclasses.dataclass(frozen=True, slots=True)
class ApprovalFailed:
    token: Token
    amount: int
    owner: AccountID
    spender: AccountID
    exception: Exception


TradeError = (
    InsufficientSourceBalance
    | QuoteFailed
    | QuoteLiquidityUnavailable
    | OrderRejected
    | RiskManagerRejection
    | ApprovalFailed  # Technically this should be a TransactionError, but ApprovableToken.approve() doesn't return events
    | SubmitOrderFailed
    | SourceNotWithdrawn
    | DestinationNotReceived
)


@dataclasses.dataclass(frozen=True, slots=True)
class CreateTransactionFailed:
    exception: Exception
    data: dict[str, Any]


@dataclasses.dataclass(frozen=True, slots=True)
class BroadcastTransactionFailed:
    transaction: Transaction
    exception: Exception
    data: dict[str, Any]


@dataclasses.dataclass(frozen=True, slots=True)
class WaitForTransactionReceiptFailed:
    transaction: SentTransaction
    exception: Exception
    data: dict[str, Any]


TransactionError = (
    CreateTransactionFailed
    | BroadcastTransactionFailed
    | WaitForTransactionReceiptFailed
)


@dataclasses.dataclass(frozen=True, slots=True)
class Trade:
    pair: tuple[Token, Token]
    quote: Quote
    order: OrderResponse


TradeEvent = Trade | TradeError | TransactionError

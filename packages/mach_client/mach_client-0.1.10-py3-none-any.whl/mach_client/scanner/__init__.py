from ..asset import Token
from ..chain import Chain
from .scanner import Scanner


def address(chain: Chain, address: str) -> str:
    return Scanner.create(chain).address(address)


def transaction(chain: Chain, transaction_id: str) -> str:
    return Scanner.create(chain).transaction(transaction_id)


def token(token: Token) -> str:
    return Scanner.create(token.chain).token(token)

from __future__ import annotations
import abc
from abc import ABC

from ..asset import Token
from ..chain import Chain, EthereumChain, SolanaChain, TronChain


class Scanner(ABC):
    @staticmethod
    def create(chain: Chain) -> Scanner:
        match chain:
            case EthereumChain() | SolanaChain():
                return EIP3091Scanner(chain)
            case TronChain():
                return TronScanner()
            case _ as chain:
                raise NotImplementedError(f"Unimplemented chain: {chain}")

    @abc.abstractmethod
    def address(self, address: str) -> str:
        pass

    @abc.abstractmethod
    def transaction(self, transaction_id: str) -> str:
        pass

    @abc.abstractmethod
    def token(self, token: Token) -> str:
        pass


# Avoid a circular import
from .eip3091 import EIP3091Scanner  # noqa: E402
from .tron import TronScanner  # noqa: E402

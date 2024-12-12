import dataclasses
from decimal import Decimal

from mach_client.asset import EthereumToken

from .rebalance_manager import RebalanceAnalysis


@dataclasses.dataclass(frozen=True, slots=True)
class RebalanceEvaluation:
    rebalance_analysis: RebalanceAnalysis


@dataclasses.dataclass(frozen=True, slots=True)
class Withdraw:
    amounts: list[tuple[EthereumToken, Decimal]]


@dataclasses.dataclass(frozen=True, slots=True)
class Supply:
    amounts: list[tuple[EthereumToken, Decimal]]


@dataclasses.dataclass(frozen=True, slots=True)
class LiquidityRateError:
    tokens: list[EthereumToken]
    exception: Exception


@dataclasses.dataclass(frozen=True, slots=True)
class WithdrawError:
    token: EthereumToken
    amount: Decimal
    exception: Exception


@dataclasses.dataclass(frozen=True, slots=True)
class ConvertError:
    src_token: EthereumToken
    error: object


@dataclasses.dataclass(frozen=True, slots=True)
class SupplyError:
    token: EthereumToken
    amount: Decimal
    exception: Exception


AaveError = LiquidityRateError | WithdrawError | ConvertError | SupplyError

AaveEvent = RebalanceEvaluation | Withdraw | Supply | AaveError
